from webapp_health_monitor.backends.system import FileSystemBackend


class ValueExtractor(object):
    def extract(self):
        raise NotImplementedError()


class DiscSpaceExtractorBase(ValueExtractor):
    def __init__(self, mount_point):
        self.backend = FileSystemBackend(mount_point)


class FreeDiskSpaceExtractor(DiscSpaceExtractorBase):
    def extract(self):
        return self.backend.free_space


class PercentUsedDiskSpaceExtractor(DiscSpaceExtractorBase):
    def extract(self):
        return self.backend.percent_used
