"""Reproduce bounded examples; author-run output is not external validation."""
import argparse
import copy
import importlib.util
import json
import tempfile
import time
from pathlib import Path

from delegation_market.mechanisms import run_auction
from delegation_market.m11_interval import certify

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='Recompute all 10,000 intervals; allow several minutes')
    args = parser.parse_args()
    started = time.perf_counter()
    first = run_auction([0.2, 0.8], 'first_price')
    second = run_auction([0.2, 0.8], 'second_price')
    if (first.winner, first.price, second.winner, second.price) != (1, 0.8, 1, 0.2):
        raise RuntimeError('Small auction example failed')
    try:
        run_auction([-0.1, 0.2])
    except ValueError:
        pass
    else:
        raise RuntimeError('Invalid bid was accepted')
    spec = importlib.util.spec_from_file_location('release_sanity', ROOT / 'scripts/check_release_sanity.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Release-sanity module unavailable')
    sanity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sanity)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / 'certificate.json'
        if args.full:
            result = certify(path)
            mode = 'RECOMPUTED_10000_INTERVALS'
        else:
            result = json.loads((ROOT / 'results/m11/constant_alpha_certificate.json').read_text())
            path.write_text(json.dumps(result))
            mode = 'COMMITTED_RECORD_CHECK_ONLY'
        sanity.check_certificate(path)
        if result.get('alpha_subintervals') != 10000 or result.get('certified') is not True:
            raise RuntimeError('Certificate did not satisfy its declared scope')
        checks = result.get('checks', {})
        if len(checks) != 6 or not all(value is True for value in checks.values()):
            raise RuntimeError('A certificate predicate failed')
        altered = copy.deepcopy(result)
        altered['witness']['eta_low'] = '0.9'
        path.write_text(json.dumps(altered))
        try:
            sanity.check_certificate(path)
        except AssertionError:
            pass
        else:
            raise RuntimeError('Altered witness was accepted')
    print(json.dumps({'scope': 'Finite authored model; not independent proof review or human behavior',
        'mode': mode, 'first_price': first.price, 'second_price': second.price,
        'negative_bid_rejected': True, 'altered_witness_rejected': True,
        'certificate': result, 'runtime_seconds': round(time.perf_counter() - started, 3)}, indent=2))


if __name__ == '__main__':
    main()
