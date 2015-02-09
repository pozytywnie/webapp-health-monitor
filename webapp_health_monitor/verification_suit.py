import collections

from webapp_health_monitor.errors import VerificationFailure


class VerificationSuit(object):
    def __init__(self,  verificators):
        self.verificators = verificators

    def run(self):
        failures = []
        errors = []
        for verificator in self.verificators:
            try:
                verificator.run()
            except VerificationFailure as e:
                failures.append(VerificatorResultFailure(verificator, e))
            except Exception as e:
                errors.append(VerificatorResultError(verificator, e))
        return VerificationSuitResult(failures=failures, errors=errors)


class VerificationSuitResult(object):
    def __init__(self, failures, errors):
        self.failures = failures
        self.errors = errors

    def report(self):
        if self.has_failed():
            message = 'Failure\n'
            if self.errors:
                message += 'Errors\n' + '\n'.join(map(str, self.errors))
            if self.failures:
                message += 'Failures\n' + '\n'.join(map(str, self.failures))
            return message
        else:
            return 'Success\n'

    def has_failed(self):
        return bool(self.errors or self.failures)


class VerificatorResultError(collections.namedtuple(
        'VerificatorResultErrorBase', ('verificator', 'error'))):
    def __str__(self):
        return '{}: {}'.format(self.verificator, repr(self.error))


class VerificatorResultFailure(collections.namedtuple(
        'VerificatorResultFailureBase', ('verificator', 'failure'))):
    def __str__(self):
        return '{}: {}'.format(self.verificator, self.failure)
