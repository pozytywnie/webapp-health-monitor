# -*- coding: utf-8 -*-

import subprocess
from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock


from webapp_health_monitor.backends.system import DiskVolume
from webapp_health_monitor.backends.system import MountPointNotFound
from webapp_health_monitor.backends.system import FileSystemINodeBackend
from webapp_health_monitor.backends.system import FileSystemMemoryBackend
from webapp_health_monitor import errors


class DiscVolumeTest(TestCase):
    def test_kilobytes(self):
        self.assertEqual(DiskVolume(2), DiskVolume.kilobytes(2))

    def test_megabytes(self):
        self.assertEqual(DiskVolume.kilobytes(2048),
                         DiskVolume.megabytes(2))

    def test_gigabytes(self):
        self.assertEqual(DiskVolume.kilobytes(2097152),
                         DiskVolume.gigabytes(2))

    def test_eq_ok(self):
        self.assertTrue(DiskVolume(1) == DiskVolume(1))

    def test_eq_bad(self):
        self.assertFalse(DiskVolume(1) == DiskVolume(2))

    def test_lt_ok(self):
        self.assertTrue(DiskVolume(1) < DiskVolume(2))

    def test_lt_bad(self):
        self.assertFalse(DiskVolume(2) < DiskVolume(2))

    def test_lte_ok(self):
        self.assertTrue(DiskVolume(2) <= DiskVolume(2))

    def test_gt_ok(self):
        self.assertTrue(DiskVolume(2) > DiskVolume(1))

    def test_gt_bad(self):
        self.assertFalse(DiskVolume(2) > DiskVolume(2))

    def test_gte_ok(self):
        self.assertTrue(DiskVolume(2) >= DiskVolume(2))


class FileSystemBackendTest(TestCase):
    def test_raise_mout_point_not_found(self):
        backend = FileSystemMemoryBackend('/')
        backend._get_mount_points_reports = mock.Mock(
            return_value=mock.MagicMock())
        self.assertRaises(MountPointNotFound,
                          backend._get_mount_point_attribute, mock.Mock())


class FileSystemMemoryBackendTest(TestCase):
    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_free_space(self, check_output):
        check_output.return_value.decode.return_value = (
            '''System plików      1K-bl    użyte dostępne %uż. zamont. na
/dev/sda1       49082176 11941684 34624168  26% /
''')
        self.assertEqual(DiskVolume.kilobytes(34624168),
                         FileSystemMemoryBackend('/').free_space)

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_used_space(self, check_output):
        check_output.return_value.decode.return_value = (
            '''System plików      1K-bl    użyte dostępne %uż. zamont. na
/dev/sda1       49082176 11941684 34624168  26% /
''')
        self.assertEqual(DiskVolume.kilobytes(11941684),
                         FileSystemMemoryBackend('/').used_space)

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_used_space(self, check_output):
        check_output.return_value.decode.return_value = (
            '''System plików      1K-bl    użyte dostępne %uż. zamont. na
/dev/sda1       49082176 11941684 34624168  26% /
''')
        self.assertEqual(26, FileSystemMemoryBackend('/').percent_used)

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_df_result(self, check_output):
        FileSystemMemoryBackend('/')._get_df_result()
        check_output.assert_called_with(['df'])
        check_output(['df']).decode.assert_called_with('utf-8')

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_encapsulates_df_error(self, check_output):
        check_output.side_effect = [subprocess.CalledProcessError(1, ['df'])]
        self.assertRaises(errors.BackendError,
                          FileSystemMemoryBackend('/')._get_df_result)


class FileSystemINodeBackendTest(TestCase):
    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_free_inodes(self, check_output):
        check_output.return_value.decode.return_value = (
            '''System plików   iwęzły  użyteI  wolneI %uż.I zamont. na
/dev/sda1      3129344  449177 2680167   15% /
''')
        self.assertEqual(2680167, FileSystemINodeBackend('/').free_inodes)

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_used_inodes(self, check_output):
        check_output.return_value.decode.return_value = (
            '''System plików   iwęzły  użyteI  wolneI %uż.I zamont. na
/dev/sda1      3129344  449177 2680167   15% /
''')
        self.assertEqual(449177, FileSystemINodeBackend('/').used_inodes)

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_used_space(self, check_output):
        check_output.return_value.decode.return_value = (
            '''System plików   iwęzły  użyteI  wolneI %uż.I zamont. na
/dev/sda1      3129344  449177 2680167   15% /
''')
        self.assertEqual(15, FileSystemINodeBackend('/').percent_used)

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_df_result(self, check_output):
        FileSystemINodeBackend('/')._get_df_result()
        check_output.assert_called_with(['df', '-i'])
        check_output(['df', '-i']).decode.assert_called_with('utf-8')

    @mock.patch('webapp_health_monitor.backends.system.subprocess.'
                'check_output')
    def test_encapsulates_df_error(self, check_output):
        check_output.side_effect = [subprocess.CalledProcessError(1, ['df', '-i'])]
        self.assertRaises(errors.BackendError,
                          FileSystemMemoryBackend('/')._get_df_result)
