from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from webapp_health_monitor import errors
from webapp_health_monitor.verificators import RangeVerificator


class RangeVerificatorTest(TestCase):
    def test_lack_of_value_extractor_raises_bad_configuration(self):
        logger = mock.Mock()
        verificator = RangeVerificator(logger)
        verificator.lower_bound = 0
        verificator.upper_bound = 0
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_lack_of_bounds_raises_bad_configuration(self):
        logger = mock.Mock()
        verificator = RangeVerificator(logger)
        verificator.value_extractor = mock.Mock()
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_bad_bounds_raises_bad_configuration(self):
        logger = mock.Mock()
        verificator = RangeVerificator(logger)
        verificator.value_extractor = mock.Mock()
        verificator.lower_bound = 1
        verificator.upper_bound = 0
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_value_below_lower_bound_raises_verification_error(self):
        logger = mock.Mock()
        verificator = RangeVerificator(logger)
        verificator.value_extractor = mock.Mock(
            extract=mock.Mock(return_value=99))
        verificator.lower_bound = 100
        self.assertRaises(errors.VerificationError, verificator.run)

    def test_value_over_upper_bound_raises_verification_error(self):
        logger = mock.Mock()
        verificator = RangeVerificator(logger)
        verificator.value_extractor = mock.Mock(
            extract=mock.Mock(return_value=100))
        verificator.upper_bound = 99
        self.assertRaises(errors.VerificationError, verificator.run)

    def test_check_logging(self):
        logger = mock.Mock()
        verificator = RangeVerificator(logger)
        verificator.value_extractor = mock.Mock(
            extract=mock.Mock(return_value=1))
        verificator.lower_bound = 0
        verificator.upper_bound = 2
        verificator.run()
        logger.check_range.assert_called_with(0, 1, 2)
