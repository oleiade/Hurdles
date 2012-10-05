# -*- coding:utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

import time

from functools import wraps
from inspect import getmembers, ismethod


def time_it(func, *args, **kwargs):
    """
    Decorator whichs times a function execution.
    """
    start = time.time()
    func(*args, **kwargs)
    end = time.time()
    exec_time = "%s (%0.3f ms)" % (func.func_name, (end - start) * 1000)

    return exec_time


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

    def run(self):
        for method_name, method_value in self.benchmarks:
            self.setUp()
            time_it(method_value, self)
            self.tearDown()

