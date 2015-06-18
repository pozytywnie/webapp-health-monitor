from optparse import make_option
import importlib
import sys

from django.apps import apps
from django.core.management.base import BaseCommand

from webapp_health_monitor.verification_suit import VerificationSuit


class Command(BaseCommand):
    SUBMODULE_NAME = 'verificators'
    option_list = BaseCommand.option_list + (
        make_option('--tag', type=str, default=[], action='append', dest='tags'),
    )

    def handle(self, tags, **kwargs):
        submodules = self._get_verificator_modules()
        for submodule in submodules:
            try:
                importlib.import_module(submodule)
            except ImportError as e:
                if not self._import_error_concerns_verificator(submodule, e):
                    raise e
        result = VerificationSuit(tags).run()
        self.stdout.write('{}\n'.format(result.report()))
        sys.exit(result.has_failed())

    def _get_verificator_modules(self):
        for app in apps.get_app_configs():
            yield '.'.join([app.module.__name__, self.SUBMODULE_NAME])

    def _import_error_concerns_verificator(self, submodule, error):
        if sys.version_info >= (3, 0):
            return str(error) == "No module named '{}'".format(submodule)
        else:
            return error.message == "No module named {}".format(
                self.SUBMODULE_NAME)
