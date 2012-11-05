# -*- coding: utf-8 -*-

import argparse


def init_parser():
    parser = argparse.ArgumentParser(
        description="Hurdles benchmark framework"
    )
    parser.add_argument('paths', metavar='P', type=str, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('-s',
                        '--sampling',
                        action='store',
                        type=int,
                        default=10)

    return parser
