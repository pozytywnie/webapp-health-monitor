import collections
import traceback
import sys

from webapp_health_monitor.errors import VerificationFailure


class VerificationSuit(object):
    def __init__(self,  verificators):
        self.verificators = verificators

    def run(self):
        results = []
        for verificator in self.verificators:
            try:
                verificator.run()
            except VerificationFailure as e:
                results.append(VerificatorResultFailure(verificator, e))
            except Exception:
                type, value, traceback = sys.exc_info()
                results.append(VerificatorResultError(
                    verificator, type, value, traceback))
            else:
                results.append(VerificatorResultSuccess(verificator))
        return VerificationSuitResult(results)


class VerificationSuitResult(object):
    def __init__(self, results):
        self.results = results

    def report(self):
        report_lines = []
        for result in self.results:
            report_lines.append(str(result))
        errors = list(self.errors)
        if errors:
            report_lines.append('')
            report_lines.append('Errors')
            for result in errors:
                report_lines.append(str(result.verificator))
                stack_trace = traceback.format_exception(
                    result.type, result.value, result.traceback)
                report_lines.append(''.join(stack_trace))
        return '\n'.join(report_lines)

    def has_failed(self):
        return bool(list(self.errors)) or bool(list(self.failures))

    @property
    def errors(self):
        for result in self.results:
            if isinstance(result, VerificatorResultError):
                yield result

    @property
    def failures(self):
        for result in self.results:
            if isinstance(result, VerificatorResultFailure):
                yield result


class VerificatorResultSuccess(object):
    def __init__(self, verificator):
        self.verificator = verificator

    def __str__(self):
        return '{}: OK'.format(self.verificator)


class VerificatorResultError(collections.namedtuple(
        'VerificatorResultErrorBase', (
            'verificator', 'type', 'value', 'traceback'))):
    def __str__(self):
        return '{}: ERROR'.format(self.verificator)


class VerificatorResultFailure(collections.namedtuple(
        'VerificatorResultFailureBase', ('verificator', 'failure'))):
    def __str__(self):
        value_description = self.verificator.value_description
        if value_description:
            return '{}: FAILURE {} {}'.format(
                self.verificator, value_description, self.failure)
        else:
            return '{}: FAILURE Value {}'.format(
                self.verificator, self.failure)

