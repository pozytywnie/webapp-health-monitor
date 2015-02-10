import argparse
import importlib
import sys

from webapp_health_monitor.verification_suit import VerificationSuit
from webapp_health_monitor.verificators import get_verificators


def webapp_health_monitor():
    return _webapp_health_monitor(sys.argv[1:])


def _webapp_health_monitor(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('module', type=str)
    args = parser.parse_args(argv)
    sys.path.append('.')
    try:
        importlib.import_module(args.module)
    except ImportError:
        return 1
    else:
        result = VerificationSuit(get_verificators()).run()
        print(result.report())
        return int(result.has_failed())
