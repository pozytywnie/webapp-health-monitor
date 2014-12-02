from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock


from webapp_health_monitor.backends.system import DiskVolume


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
