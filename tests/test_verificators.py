from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from webapp_health_monitor import errors
from webapp_health_monitor.verificators.base import RangeVerificator
from webapp_health_monitor.verificators.system import FreeDiskSpaceVerificator
from webapp_health_monitor.verificators.system import (
    PercentUsedDiskSpaceVerificator)


class RangeVerificatorTest(TestCase):
    def test_lack_of_value_extractor_raises_bad_configuration(self):
        verificator = RangeVerificator()
        verificator.lower_bound = 0
        verificator.upper_bound = 0
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_lack_of_bounds_raises_bad_configuration(self):
        verificator = RangeVerificator()
        verificator.value_extractor = mock.Mock()
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_bad_bounds_raises_bad_configuration(self):
        verificator = RangeVerificator()
        verificator.value_extractor = mock.Mock()
        verificator.lower_bound = 1
        verificator.upper_bound = 0
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_value_below_lower_bound_raises_verification_error(self):
        verificator = RangeVerificator()
        verificator._get_value = mock.Mock(return_value=99)
        verificator.value_extractor = mock.Mock()
        verificator.lower_bound = 100
        self.assertRaises(errors.VerificationError, verificator.run)

    def test_value_over_upper_bound_raises_verification_error(self):
        verificator = RangeVerificator()
        verificator._get_value = mock.Mock(return_value=100)
        verificator.value_extractor = mock.Mock()
        verificator.upper_bound = 99
        self.assertRaises(errors.VerificationError, verificator.run)

    def test_get_value(self):
        verificator = RangeVerificator()
        verificator.value_extractor = mock.Mock(
            extract=mock.Mock(return_value=1))
        self.assertEqual(1, verificator._get_value())


class FreeDiskSpaceVerificatorTest(TestCase):
    @mock.patch('webapp_health_monitor.verificators.system.'
                'FreeDiskSpaceExtractor')
    def test_using_value_extractor(self, FreeDiskSpaceExtractor):
        class AppVerificator(FreeDiskSpaceVerificator):
            mount_point = '/home'
        verificator = AppVerificator()
        FreeDiskSpaceExtractor.return_value.extract.return_value = 100
        self.assertEqual(100, verificator._get_value())
        FreeDiskSpaceExtractor.assert_called_with('/home')


class PercentUsedDiskSpaceVerificatorTest(TestCase):
    @mock.patch('webapp_health_monitor.verificators.system.'
                'PercentUsedDiskSpaceExtractor')
    def test_using_value_extractor(self, PercentUsedDiskSpaceExtractor):
        class AppVerificator(PercentUsedDiskSpaceVerificator):
            mount_point = '/home'
        verificator = AppVerificator()
        PercentUsedDiskSpaceExtractor.return_value.extract.return_value = 100
        self.assertEqual(100, verificator._get_value())
        PercentUsedDiskSpaceExtractor.assert_called_with('/home')
