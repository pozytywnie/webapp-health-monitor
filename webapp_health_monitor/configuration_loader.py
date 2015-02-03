import importlib
import sys
from webapp_health_monitor.errors import BadConfigurationError

from webapp_health_monitor.verification_suit import VerificationSuit


class ConfigurationLoader(object):
    def load(self, file):
        module = self._import_module(file)
        verification_suit = self._get_verification_suit(module)
        return verification_suit

    def _import_module(self, file):
        try:
            sys.path.append('.')
            return importlib.import_module(file)
        except ImportError:
            raise ValueError

    def _get_verification_suit(self, module):
        try:
            return VerificationSuit(module.VERIFICATORS)
        except AttributeError:
            raise BadConfigurationError
