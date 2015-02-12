from webapp_health_monitor.backends.system import FileSystemBackend
from webapp_health_monitor.verificators.base import RangeVerificator


class FreeDiskSpaceVerificator(RangeVerificator):
    value_description = 'Free disk space'
    mount_point = '/'

    def __init__(self, *args, **kwargs):
        super(FreeDiskSpaceVerificator, self).__init__(*args, **kwargs)
        self.backend = FileSystemBackend(self.mount_point)

    def get_value(self):
        return self.backend.free_space


class PercentUsedDiskSpaceVerificator(RangeVerificator):
    value_description = 'Percent disk used'
    mount_point = '/'

    def __init__(self, *args, **kwargs):
        super(PercentUsedDiskSpaceVerificator, self).__init__(*args, **kwargs)
        self.backend = FileSystemBackend(self.mount_point)

    def get_value(self):
        return self.backend.percent_used
