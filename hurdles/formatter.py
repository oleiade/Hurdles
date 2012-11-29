# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

from clint.textui import indent, puts, colored


class Formatter(object):
    def __init__(self, output='stdout', scale='ms', *args, **kwargs):
        self.HANDLERS = {
            'stdout': self.to_stdout,
            'tsv': self.to_tsv,
        }
        self.scale = scale
        self.output = output.lower()
        if not output in self.HANDLERS:
            raise KeyError("Output type : %s is not handled. Yet." % output)

    def apply(self, benchcase_it, classname, *args, **kwargs):
        return self.HANDLERS[self.output](benchcase_it, classname, *args, **kwargs)

    def to_stdout(self, benchcase_it, classname, *args, **kwargs):
        ran = 0

        for method, times, stats in benchcase_it:
            puts("{0}.{1}".format(classname, method))
            with indent(3, quote=colored.yellow(' |')):
                for key, value in stats._asdict().items():
                    puts('{0}\t {1} {2}'.format(key, value, self.scale))
            ran += 1

        return ran, None

    def to_tsv(self, benchcase_it, classname, *args, **kwargs):
        path = kwargs.get('path')
        ran = 0
        action = puts

        if path:
            f = open(path, 'wb')  # let it raise if OSError
            action = f.write

        action('benchcase.method,average,median,fastest,slowest')

        for method, times, stats in benchcase_it:
            bench_name = '.'.join([classname, method])
            values = '\t'.join([unicode(value) for value
                               in stats._asdict().values()])
            action('\t'.join([bench_name, values]))
            ran += 1

        return ran
