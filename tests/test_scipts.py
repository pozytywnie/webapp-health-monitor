from unittest import TestCase
from webapp_health_monitor.scripts import _webapp_health_monitor
from webapp_health_monitor import verificators_register

try:
    from unittest import mock
except ImportError:
    import mock


class WebbappHealthMonitorTest(TestCase):
    @mock.patch('sys.stderr')
    @mock.patch('sys.stdout')
    def test_no_arguments(self, stdout, stderr):
        self.assertRaises(SystemExit, _webapp_health_monitor, [])

    @mock.patch('sys.stdout')
    @mock.patch('webapp_health_monitor.scripts.importlib.import_module')
    def test_import(self, import_module, stdout):
        import_module.side_effect = ImportError()
        self.assertRaises(ImportError,
                          _webapp_health_monitor, ['random_module'])
        import_module.assert_called_with('random_module')

    @mock.patch('webapp_health_monitor.scripts.importlib.import_module')
    def test_no_verificators(self, import_module):
        with mock.patch('sys.stdout') as stdout:
            result = _webapp_health_monitor(['random_module'])
        self.assertEqual(1, result)
        self.assertEqual([mock.call('No verificators found.\n\n')],
                         stdout.write.mock_calls)

    @mock.patch('webapp_health_monitor.scripts.importlib.import_module')
    def test_success(self, import_module):
        verificator = mock.Mock()
        verificators_register.register(verificator)
        with mock.patch('sys.stdout') as stdout:
            result = _webapp_health_monitor(['random_module'])
        self.assertEqual(0, result)
        self.assertEqual(
            [mock.call('{}: OK\n'.format(verificator.return_value))],
            stdout.write.mock_calls)
