import traceback
import sys
from webapp_health_monitor.actions import get_actions

from webapp_health_monitor.errors import VerificationFailure
from webapp_health_monitor import verificators_register


class VerificationSuit(object):
    def __init__(self, tags):
        self.tags = tags

    def run(self):
        results = []
        for verificator in verificators_register.get_verificators(self.tags):
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
        verification_result = VerificationSuitResult(results)
        if verification_result.has_failed():
            for action in get_actions():
                action.run(verification_result)
        return verification_result


class VerificationSuitResult(object):
    def __init__(self, results):
        self.results = results

    def report(self):
        if self.results:
            report_lines = []
            for result in self.results:
                report_lines.append(str(result))
            failures = list(self.failures)
            if failures:
                report_lines.append('')
                report_lines.append('Failures')
                for result in failures:
                    report_lines.extend(result.long_description)
            errors = list(self.errors)
            if errors:
                report_lines.append('')
                report_lines.append('Errors')
                for result in errors:
                    report_lines.extend(result.long_description)
            return '\n'.join(report_lines)
        else:
            return 'No verificators found.\n'

    def has_failed(self):
        return bool(list(self.errors)) or bool(list(self.failures)) or not self.results

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


class VerificatorResultError(object):
    def __init__(self, verificator, type_, value, traceback_):
        self.verificator = verificator
        self.type = type_
        self.value = value
        self.traceback = traceback_

    def __str__(self):
        return '{}: ERROR'.format(self.verificator)

    @property
    def long_description(self):
        stacktrace = traceback.format_exception(
            self.type, self.value, self.traceback)
        cleared_stacktrace = [''.join(line.rsplit('\n', 1))
                              for line in stacktrace]
        return [str(self.verificator)] + cleared_stacktrace


class VerificatorResultFailure(object):
    def __init__(self, verificator, failure):
        self.verificator = verificator
        self.failure = failure

    def __str__(self):
        return '{}: FAILURE'.format(self.verificator)

    @property
    def long_description(self):
        value_description = self.verificator.value_description
        if value_description:
            description = ['{}: {} {}'.format(
                self.verificator, value_description, self.failure)]
        else:
            description = ['{}: Value {}'.format(
                self.verificator, self.failure)]
        extra_failure_report = self.verificator.extra_failure_raport()
        if extra_failure_report:
            description.append(extra_failure_report)
        return description
