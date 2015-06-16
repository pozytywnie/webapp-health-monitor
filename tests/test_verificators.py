from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from webapp_health_monitor import errors
from webapp_health_monitor.verificators.base import RangeVerificator
from webapp_health_monitor.verificators_set import VerificatorsSet
from webapp_health_monitor.verificators.system import FreeDiskSpaceVerificator
from webapp_health_monitor.verificators.system import (
    PercentUsedDiskSpaceVerificator)


class RegisterTest(TestCase):
    def test_get_precise_tag(self):
        verificator_class = mock.Mock()
        verificators_set = VerificatorsSet()
        verificators_set.register(verificator_class, ['a', 'b', 'c', 'd'])
        self.assertIn(verificator_class.return_value,
                      verificators_set.get_verificators(['a']))

    def test_get_different_tag(self):
        verificator_class = mock.Mock()
        verificators_set = VerificatorsSet()
        verificators_set.register(verificator_class, ['b', 'c', 'd'])
        self.assertNotIn(verificator_class.return_value,
                         verificators_set.get_verificators(['a']))

    def test_get_without_tag_on_tagged(self):
        verificator_class = mock.Mock()
        verificators_set = VerificatorsSet()
        verificators_set.register(verificator_class, ['a'])
        self.assertIn(verificator_class.return_value,
                      verificators_set.get_verificators([]))

    def test_get_without_tag_on_untagged(self):
        verificator_class = mock.Mock()
        verificators_set = VerificatorsSet()
        verificators_set.register(verificator_class)
        self.assertIn(verificator_class.return_value,
                      verificators_set.get_verificators([]))

    def test_get_tag_on_untagged(self):
        verificator_class = mock.Mock()
        verificators_set = VerificatorsSet()
        verificators_set.register(verificator_class)
        self.assertNotIn(verificator_class.return_value,
                         verificators_set.get_verificators(['a']))


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
