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
        range_checker = self._validate_range()
        range_checker.check(self.get_value())

    def _validate_range(self):
        lower_bound = self.get_lower_bound()
        upper_bound = self.get_upper_bound()

        if lower_bound is None:
            if upper_bound is None:
                raise errors.BadConfigurationError(
                    "Range verification require at least one bound set")
            else:
                return UpperBoundChecker(upper_bound)
        else:
            if upper_bound is None:
                return LowerBoundChecker(lower_bound)
            else:
                if lower_bound < upper_bound:
                    return RangeChecker(lower_bound, upper_bound)
                else:
                    raise errors.BadConfigurationError(
                        "Lower bound must be less then upper bound")

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

    def get_value(self):
        raise NotImplementedError


class RangeCheckerBase:
    def check(self, value):
        raise NotImplementedError


class RangeChecker(RangeCheckerBase):
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def check(self, value):
        if self.lower_bound <= value <= self.upper_bound:
            return
        else:
            raise errors.VerificationFailure()


class LowerBoundChecker(RangeCheckerBase):
    def __init__(self, bound):
        self.bound = bound

    def check(self, value):
        if self.bound <= value:
            return
        else:
            raise errors.VerificationFailure()


class UpperBoundChecker(RangeCheckerBase):
    def __init__(self, bound):
        self.bound = bound

    def check(self, value):
        if value <= self.bound:
            return
        else:
            raise errors.VerificationFailure()
