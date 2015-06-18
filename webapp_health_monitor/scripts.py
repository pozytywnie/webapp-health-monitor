import argparse
import importlib
import sys

from webapp_health_monitor.verification_suit import VerificationSuit


def webapp_health_monitor():
    sys.exit(_webapp_health_monitor(sys.argv[1:]))


def _webapp_health_monitor(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('module', type=str)
    parser.add_argument('--tag', type=str, default=[], action='append', dest='tags')
    args = parser.parse_args(argv)
    sys.path.append('.')
    importlib.import_module(args.module)
    result = VerificationSuit(args.tags).run()
    sys.stdout.write('{}\n'.format(result.report()))
    return int(result.has_failed())
