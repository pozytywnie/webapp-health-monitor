from unittest import TestCase
from datetime import datetime

try:
    from unittest import mock
except ImportError:
    import mock

from webapp_health_monitor.verification_suit import VerificatorResultError
from webapp_health_monitor.verification_suit import VerificatorResultFailure
from webapp_health_monitor.verification_suit import VerificationSuit
from webapp_health_monitor.verification_suit import VerificationSuitResult
from webapp_health_monitor.verification_suit import VerificationFailure


class VerificationSuitTest(TestCase):
    def test_success(self):
        verificator = mock.Mock()
        verification_result = VerificationSuit([verificator]).run()
        self.assertEqual([], verification_result.errors)
        self.assertEqual([], verification_result.failures)

    def test_failure(self):
        verification_error = VerificationFailure()
        verificator = mock.Mock(run=mock.Mock(side_effect=verification_error))
        verification_result = VerificationSuit([verificator]).run()
        self.assertEqual(
            [VerificatorResultFailure(verificator, verification_error)],
            verification_result.failures)

    def test_error(self):
        error = Exception()
        verificator = mock.Mock(run=mock.Mock(side_effect=error))
        verification_result = VerificationSuit([verificator]).run()
        self.assertEqual([VerificatorResultError(verificator, error)],
                         verification_result.errors)
        self.assertEqual([], verification_result.failures)


class VerificationSuitResultTest(TestCase):
    def test_has_failed_ok(self):
        verification_suit = VerificationSuitResult(errors=[], failures=[])
        self.assertFalse(verification_suit.has_failed())

    def test_has_failed_error(self):
        verification_suit = VerificationSuitResult(
            errors=[VerificationFailure()], failures=[])
        self.assertTrue(verification_suit.has_failed())

    def test_has_failed_fail(self):
        verification_suit = VerificationSuitResult(
            errors=[], failures=[Exception])
        self.assertTrue(verification_suit.has_failed())
