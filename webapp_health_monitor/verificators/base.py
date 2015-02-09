from webapp_health_monitor import errors


class Verificator(object):
    verificator_name = None

    def __init__(self, **kwargs):
        pass

    def run(self):
        raise NotImplementedError()

    def __str__(self):
        if self.verificator_name:
            return self.verificator_name
        else:
            return self.__class__.__name__


class RangeVerificator(Verificator):
    upper_bound = None
    lower_bound = None

    def run(self):
        self._check_configuration()
        self._check_value()

    def _check_configuration(self):
        if not self._are_bounds_configured():
            raise errors.BadConfigurationError()

    def _are_bounds_configured(self):
        if self.lower_bound is None:
            return self.upper_bound is not None
        elif self.upper_bound is not None:
            return self.lower_bound <= self.upper_bound
        else:
            return True

    def _check_value(self):
        value = self.get_value()
        self._check_lower_bound(value)
        self._check_upper_bound(value)

    def get_value(self):
        raise NotImplementedError

    def _check_lower_bound(self, value):
        if self.lower_bound is not None:
            if value < self.lower_bound:
                raise errors.VerificationFailure()

    def _check_upper_bound(self, value):
        if self.upper_bound is not None:
            if value > self.upper_bound:
                raise errors.VerificationFailure()
