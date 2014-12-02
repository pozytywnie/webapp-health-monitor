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
        return '{} kB'.format(self._kilobytes)
