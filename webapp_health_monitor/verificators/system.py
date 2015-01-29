from webapp_health_monitor.backends.system import FileSystemBackend
from webapp_health_monitor.verificators.base import RangeVerificator


class FreeDiskSpaceVerificator(RangeVerificator):
    mount_point = '/'

    def __init__(self, *args, **kwargs):
        super(FreeDiskSpaceVerificator, self).__init__(*args, **kwargs)
        self.backend = FileSystemBackend(self.mount_point)

    def _get_value(self):
        return self.backend.free_space


class PercentUsedDiskSpaceVerificator(RangeVerificator):
    mount_point = '/'

    def __init__(self, *args, **kwargs):
        super(PercentUsedDiskSpaceVerificator, self).__init__(*args, **kwargs)
        self.backend = FileSystemBackend(self.mount_point)

    def _get_value(self):
        return self.backend.percent_used
