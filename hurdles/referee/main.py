# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

from hurdles.referee.actions import get_bench_from_cmdline, discover_benchmarks

from .args import init_parser


def main():
    args = init_parser().parse_args(sys.argv[1:])
    benchmarks = discover_benchmarks(get_bench_from_cmdline(args.paths))

    for bench in benchmarks:
        bench().run(args.sampling)

    sys.stdout.write('\n' + ('-' * 60) + '\n\n')
    sys.stdout.write('Done.\n\n')
