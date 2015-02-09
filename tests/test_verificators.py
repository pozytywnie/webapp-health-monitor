from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from webapp_health_monitor import errors
from webapp_health_monitor.verificators import _registered_verificators_classes
from webapp_health_monitor.verificators.base import RangeVerificator
from webapp_health_monitor.verificators import get_verificators
from webapp_health_monitor.verificators import register
from webapp_health_monitor.verificators.system import FreeDiskSpaceVerificator
from webapp_health_monitor.verificators.system import (
    PercentUsedDiskSpaceVerificator)


class RegisterTest(TestCase):
    def test_register(self):
        verificator_class = mock.Mock()
        register(verificator_class)
        self.assertIn(verificator_class, _registered_verificators_classes)

    def test_get_verificators(self):
        verificator_class = mock.Mock()
        register(verificator_class)
        self.assertIn(verificator_class.return_value,
                      get_verificators())


class RangeVerificatorTest(TestCase):
    def test_lack_of_bounds_raises_bad_configuration(self):
        verificator = RangeVerificator()
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_bad_bounds_raises_bad_configuration(self):
        verificator = RangeVerificator()
        verificator.lower_bound = 1
        verificator.upper_bound = 0
        self.assertRaises(errors.BadConfigurationError, verificator.run)

    def test_value_below_lower_bound_raises_verification_error(self):
        verificator = RangeVerificator()
        verificator.get_value = mock.Mock(return_value=99)
        verificator.lower_bound = 100
        self.assertRaises(errors.VerificationFailure, verificator.run)

    def test_value_over_upper_bound_raises_verification_error(self):
        verificator = RangeVerificator()
        verificator.get_value = mock.Mock(return_value=100)
        verificator.upper_bound = 99
        self.assertRaises(errors.VerificationFailure, verificator.run)

    def test_run(self):
        verificator = RangeVerificator()
        verificator.get_value = mock.Mock(return_value=1)
        verificator.lower_bound = 0
        verificator.upper_bound = 2
        verificator.run()
        self.assertTrue(verificator.get_value.called)


class FreeDiskSpaceVerificatorTest(TestCase):
    @mock.patch('webapp_health_monitor.verificators.system.'
                'FileSystemBackend')
    def test_using_file_system(self, FileSystemBackend):
        class AppVerificator(FreeDiskSpaceVerificator):
            mount_point = '/home'
        verificator = AppVerificator()
        FileSystemBackend.return_value.free_space = 100
        self.assertEqual(100, verificator.get_value())
        FileSystemBackend.assert_called_with('/home')


class PercentUsedDiskSpaceVerificatorTest(TestCase):
    @mock.patch('webapp_health_monitor.verificators.system.'
                'FileSystemBackend')
    def test_using_file_system(self, FileSystemBackend):
        class AppVerificator(PercentUsedDiskSpaceVerificator):
            mount_point = '/home'
        verificator = AppVerificator()
        FileSystemBackend.return_value.percent_used = 100
        self.assertEqual(100, verificator.get_value())
        FileSystemBackend.assert_called_with('/home')
