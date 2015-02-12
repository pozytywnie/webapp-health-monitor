from unittest import TestCase
from datetime import datetime
from webapp_health_monitor.errors import VerificationFailure

try:
    from unittest import mock
except ImportError:
    import mock

from webapp_health_monitor.verification_suit import VerificatorResultError, \
    VerificatorResultSuccess
from webapp_health_monitor.verification_suit import VerificatorResultFailure
from webapp_health_monitor.verification_suit import VerificationSuit
from webapp_health_monitor.verification_suit import VerificationSuitResult


class VerificationSuitTest(TestCase):
    def test_success(self):
        verificator = mock.Mock()
        verification_result = VerificationSuit([verificator]).run()
        self.assertEqual([], list(verification_result.errors))
        self.assertEqual([], list(verification_result.failures))

    def test_failure(self):
        verification_error = VerificationFailure()
        verificator = mock.Mock(run=mock.Mock(side_effect=verification_error))
        verification_result = VerificationSuit([verificator]).run()
        failure_report = list(verification_result.failures)[0]
        self.assertEqual(verificator, failure_report.verificator)
        self.assertEqual(verification_error, failure_report.failure)
        self.assertEqual([], list(verification_result.errors))

    def test_error(self):
        error = NotImplementedError('value')
        verificator = mock.Mock(run=mock.Mock(side_effect=error))
        verification_result = VerificationSuit([verificator]).run()
        error_report = list(verification_result.errors)[0]
        self.assertEqual(verificator, error_report.verificator)
        self.assertEqual(NotImplementedError, error_report.type)
        self.assertEqual(error, error_report.value)
        self.assertEqual([], list(verification_result.failures))


class VerificationSuitResultTest(TestCase):
    def test_has_failed_ok(self):
        verificator = mock.Mock()
        verification_suit = VerificationSuitResult(
            [VerificatorResultSuccess(verificator)])
        self.assertFalse(verification_suit.has_failed())

    def test_has_failed_error(self):
        verificator = mock.Mock()
        error_type = mock.Mock()
        value = mock.Mock()
        traceback = mock.Mock()
        verification_suit = VerificationSuitResult([
            VerificatorResultError(verificator, error_type, value, traceback)])
        self.assertTrue(verification_suit.has_failed())

    def test_has_failed_fail(self):
        verificator = mock.Mock()
        failure = mock.Mock()
        verification_suit = VerificationSuitResult(
            [VerificatorResultFailure(verificator, failure)])
        self.assertTrue(verification_suit.has_failed())
