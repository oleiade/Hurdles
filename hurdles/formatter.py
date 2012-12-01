# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

import tablib

from clint.textui import indent, puts, colored


class Formatter(object):
    def __init__(self, output='stdout', scale='ms', *args, **kwargs):
        self.scale = scale
        self.output = output.lower()

    def apply(self, benchcase_it, classname, *args, **kwargs):
        format = kwargs.get('format') or self.format

        if format == 'stdout':
            return self.to_stdout(benchcase_it, classname, *args, **kwargs)
        else:
            ran, dataset = self.format(benchcase_it, classname, *args, **kwargs)

            if hasattr(dataset, format):
                print getattr(dataset, format)
                return ran

        return 0

    def format(self, benchcase_it, classname, *args, **kwargs):
        ran = 0
        data = []
        headers = (
            'benchcase.method',
            'average',
            'median',
            'fastest',
            'slowest',
        )

        for method, times, stats in benchcase_it:
            bench_name = '.'.join([classname, method])
            values = [value for value
                      in stats._asdict().values()]
            data.append([bench_name] + values)
            ran += 1

        data = tablib.Dataset(*data, headers=headers)
        return ran, data

    def to_stdout(self, benchcase_it, classname, *args, **kwargs):
        ran = 0

        for method, times, stats in benchcase_it:
            puts("{0}.{1}".format(classname, method))
            with indent(3, quote=colored.yellow(' |')):
                for key, value in stats._asdict().items():
                    puts('{0}\t {1} {2}'.format(key, value, self.scale))
            ran += 1

        return ran
