import argparse
import importlib
import sys

from webapp_health_monitor.verification_suit import VerificationSuit
from webapp_health_monitor.verificators import get_verificators


def webapp_health_monitor():
    parser = argparse.ArgumentParser()
    parser.add_argument('module', type=str)
    args = parser.parse_args()
    sys.path.append('.')
    importlib.import_module(args.module)
    result = VerificationSuit(get_verificators()).run()
    print(result.report())
