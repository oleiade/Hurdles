# -*- coding:utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

import sys
import time

from collections import namedtuple
from functools import wraps
from inspect import getmembers, ismethod


ExecTimeCollection = namedtuple('ExecTimeCollection', ['times', 'scale'])


def extra_setup(setup_code):
    """Allows to setup some extra context to it's decorated function.

    As a convention, the bench decorated function should always handle
    *args and **kwargs. Kwargs will be updated with the extra context
    set by the decorator.

    Example:
        @extra_setup("l = [x for x in xrange(100)]")
        def bench_len(self, *args, **kwargs):
            print len(kwargs['l'])
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            exec setup_code in {}, kwargs
            return func(*args, **kwargs)
        return decorated_function
    return decorator


class BenchCase(object):
    def __init__(self):
        self._benchmarks = []
        self.results = {
            'exec_times': {},
            'averages': {},
        }

    def setUp(self):
        """Hook method for setting up the benchmark
        fixture before exercising it."""
        pass

    def tearDown(self):
        """Hook method for deconstructing the benchmark
        fixture after testing it."""
        pass

    @property
    def benchmarks(self):
        if not self._benchmarks:
            bench_case_methods = getmembers(self.__class__, predicate=ismethod)
            for (method_name, method_value) in bench_case_methods:
                if method_name.startswith('bench_'):
                    self._benchmarks.append((method_name, method_value))
        return self._benchmarks

    def tick(self, func, *args, **kwargs):
        """Times a function execution in miliseconds"""
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        exec_time = round(((end - start) * 1000), 2)

        return exec_time

    def run(self, repeat=10):
        for method_name, method_value in self.benchmarks:
            self.setUp()

            exec_times = ExecTimeCollection(times=[self.tick(method_value, self) for x in [0.0] * repeat],
                                                              scale='ms')
            average = sum(exec_times.times) / repeat
            ref_class = self.__class__.__name__

            sys.stdout.write("{0}.{1} ... {2} {3}\n".format(ref_class,
                                                                            method_name,
                                                                            average,
                                                                            exec_times.scale))

            self.results['exec_times'].update({method_name: exec_times})
            self.results['averages'].update({method_name: average})

            self.tearDown()
