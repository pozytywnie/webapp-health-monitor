from webapp_health_monitor.value_extractors import FreeDiskSpaceExtractor
from webapp_health_monitor.value_extractors import (
    PercentUsedDiskSpaceExtractor)
from webapp_health_monitor.verificators.base import RangeVerificator


class FreeDiskSpaceVerificator(RangeVerificator):
    mount_point = '/'

    def __init__(self, *args, **kwargs):
        super(FreeDiskSpaceVerificator, self).__init__(*args, **kwargs)
        self.value_extractor = FreeDiskSpaceExtractor(self.mount_point)


class PercentUsedDiskSpaceVerificator(RangeVerificator):
    mount_point = '/'

    def __init__(self, *args, **kwargs):
        super(PercentUsedDiskSpaceVerificator, self).__init__(*args, **kwargs)
        self.value_extractor = PercentUsedDiskSpaceExtractor(self.mount_point)
