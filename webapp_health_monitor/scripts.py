import argparse
import importlib
import sys

from webapp_health_monitor.verification_suit import VerificationSuit


def webapp_health_monitor():
    return _webapp_health_monitor(sys.argv[1:])


def _webapp_health_monitor(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('module', type=str)
    args = parser.parse_args(argv)
    sys.path.append('.')
    importlib.import_module(args.module)
    result = VerificationSuit().run()
    print(result.report())
    return int(result.has_failed())
