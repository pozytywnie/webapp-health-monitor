import subprocess
import collections
import re

from webapp_health_monitor import errors

MountPointMemoryReport = collections.namedtuple('MountPointMemoryReport', [
    'mount_point', 'used_space', 'free_space', 'percent_used'])

MountPointINodeReport = collections.namedtuple('MountPointInodeReport', [
    'mount_point', 'used_inodes', 'free_inodes', 'percent_used'])


class FileSystemBackendBase(object):
    def __init__(self, mount_point):
        self.mount_point = mount_point

    @property
    def df_command(self):
        raise NotImplementedError

    def _get_mount_point_attribute(self, attribute):
        for report in self._get_mount_points_reports():
            if report.mount_point == self.mount_point:
                return getattr(report, attribute)
        raise MountPointNotFound(self.mount_point)

    def _get_mount_points_reports(self):
        output = self._get_df_result()
        for line in output.splitlines()[1:]:
            yield self._parse_df_line(line)

    def _parse_df_line(self, line):
        raise NotImplementedError

    def _get_df_result(self):
        try:
            return subprocess.check_output(self.df_command).decode('utf-8')
        except subprocess.CalledProcessError:
            raise errors.BackendError()

    def _parse_percent(self, string):
        match = re.match(r'^(\d+)%$', string)
        if match:
            return int(match.groups()[0])


class FileSystemMemoryBackend(FileSystemBackendBase):
    df_command = ['df']

    @property
    def free_space(self):
        return self._get_mount_point_attribute('free_space')

    @property
    def used_space(self):
        return self._get_mount_point_attribute('used_space')

    @property
    def percent_used(self):
        return self._get_mount_point_attribute('percent_used')

    def _parse_df_line(self, line):
        _, _, used_str, free_str, percent_str, mount_point = line.split()
        percent_used = self._parse_percent(percent_str)
        free_space = DiskVolume.kilobytes(int(free_str))
        used_space = DiskVolume.kilobytes(int(used_str))
        return MountPointMemoryReport(
            mount_point=mount_point, free_space=free_space,
            used_space=used_space, percent_used=percent_used)


class FileSystemINodeBackend(FileSystemBackendBase):
    df_command = ['df', '-i']

    @property
    def free_inodes(self):
        return self._get_mount_point_attribute('free_inodes')

    @property
    def used_inodes(self):
        return self._get_mount_point_attribute('used_inodes')

    @property
    def percent_used(self):
        return self._get_mount_point_attribute('percent_used')

    def _parse_df_line(self, line):
        _, _, used_str, free_str, percent_str, mount_point = line.split()
        percent_used = self._parse_percent(percent_str)
        free_inodes = int(free_str)
        used_inodes = int(used_str)
        return MountPointINodeReport(
            mount_point=mount_point, free_inodes=free_inodes,
            used_inodes=used_inodes, percent_used=percent_used)


class DiskVolume(object):
    def __init__(self, kilobytes):
        self._kilobytes = kilobytes

    @classmethod
    def kilobytes(cls, kilobytes):
        return cls(kilobytes)

    @classmethod
    def megabytes(cls, megabytes):
        return cls.kilobytes(megabytes * 1024)

    @classmethod
    def gigabytes(cls, gigabytes):
        return cls.megabytes(gigabytes * 1024)

    def __lt__(self, other):
        return self._kilobytes < other._kilobytes

    def __le__(self, other):
        return self._kilobytes <= other._kilobytes

    def __eq__(self, other):
        return self._kilobytes == other._kilobytes

    def __str__(self):
        if self._kilobytes < 1024:
            return '{} kB'.format(self._kilobytes)
        elif self._kilobytes < 1024 * 1024:
            return '{} MB'.format(self._kilobytes / 1024)
        else:
            return '{} GB'.format(self._kilobytes / 1024 / 1024)


class MountPointNotFound(errors.VerificationFailure):
    def __init__(self, mount_point):
        super(MountPointNotFound, self).__init__(
            'Mount point {}, not found'.format(mount_point))
