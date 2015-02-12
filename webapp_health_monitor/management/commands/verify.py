import importlib

from django.apps import apps
from django.core.management.base import BaseCommand

from webapp_health_monitor.verification_suit import VerificationSuit


class Command(BaseCommand):
    SUBMODULE_NAME = 'verificators'

    def handle(self, *args, **options):
        submodules = self._get_verificator_modules()
        for submodule in submodules:
            try:
                importlib.import_module(submodule)
            except ImportError as e:
                if str(e) != "No module named '{}'".format(submodule):
                    raise e
        result = VerificationSuit().run()
        print(result.report())

    def _get_verificator_modules(self):
        for app in apps.get_app_configs():
            yield '.'.join([app.module.__name__, self.SUBMODULE_NAME])
