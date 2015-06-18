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
    @mock.patch('webapp_health_monitor.verificators_register.get_verificators')
    def test_success(self, get_verificators):
        verificator = mock.Mock()
        get_verificators.return_value = [verificator]
        verification_result = VerificationSuit([]).run()
        self.assertEqual([], list(verification_result.errors))
        self.assertEqual([], list(verification_result.failures))

    @mock.patch('webapp_health_monitor.verificators_register.get_verificators')
    def test_failure(self, get_verificators):
        verification_error = VerificationFailure()
        verificator = mock.Mock(run=mock.Mock(side_effect=verification_error))
        get_verificators.return_value = [verificator]
        verification_result = VerificationSuit([]).run()
        failure_report = list(verification_result.failures)[0]
        self.assertEqual(verificator, failure_report.verificator)
        self.assertEqual(verification_error, failure_report.failure)
        self.assertEqual([], list(verification_result.errors))

    @mock.patch('webapp_health_monitor.verificators_register.get_verificators')
    def test_error(self, get_verificators):
        error = NotImplementedError('value')
        verificator = mock.Mock(run=mock.Mock(side_effect=error))
        get_verificators.return_value = [verificator]
        verification_result = VerificationSuit([]).run()
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
