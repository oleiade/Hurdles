# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

from __future__ import absolute_import

import sys

from hurdles.referee.actions import get_bench_from_cmdline, discover_benchmarks

from .args import init_parser


def main():
    args = init_parser().parse_args(sys.argv[1:])
    benchmarks = discover_benchmarks(get_bench_from_cmdline(args.paths))
    ran_benchmarks = 0

    for bench in benchmarks:
        bench().run(sampling=args.sampling)
        ran_benchmarks += 1

    closure_msg = '\n{0} \nRan {1} benchmarks \n\nDone.'.format(('-' * 60), ran_benchmarks)
    sys.stdout.write(closure_msg)
