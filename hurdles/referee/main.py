# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

from __future__ import absolute_import

import sys

from hurdles.base import BenchSuite

from .actions import get_bench_from_cmdline, discover_benchcases
from .args import init_parser


def main():
    args = init_parser().parse_args(sys.argv[1:])
    benchcases = discover_benchcases(get_bench_from_cmdline(args.paths))
    suite = BenchSuite()
    ran_benchmarks = 0

    for benchcase in benchcases:
        suite.add_benchcase(benchcase())

    ran_benchmarks = suite.run(sampling=args.sampling,
                               format=args.format)

    if args.format == 'stdout':
        closure_msg = '\n{0} \nRan {1} benchmarks \n\nDone.'.format(('-' * 60), ran_benchmarks)
        sys.stdout.write(closure_msg)
