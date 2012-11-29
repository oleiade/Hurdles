# -*- coding:utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

import sys
import time

from collections import namedtuple
from inspect import getmembers, ismethod

from clint.textui import indent, puts, colored

from .formatter import Formatter
from .utils import median, average


ExecutionStats = namedtuple('ExecutionStats', ['average', 'median', 'fastest', 'slowest'])
ExecTimeCollection = namedtuple('ExecTimeCollection', ['times', 'scale'])


class InvalidBenchmarkError(Exception):
    pass


class BenchCase(object):
    scale = 'ms'

    def __init__(self, methods=None):
        self.formatter = Formatter()
        self.results = {
            'times': {},
            'stats': {},
        }
        self._benchmarks = self._select(methods) if methods else None

    def setUp(self):
        """Hook method for setting up the benchmark
        fixture before exercising it."""
        pass

    def tearDown(self):
        """Hook method for deconstructing the benchmark
        fixture after testing it."""
        pass

    def _select(self, methods):
        methods = [methods] if isinstance(methods, str) else methods
        bench_cases_methods = []

        for method_name in methods:
            if hasattr(self, method_name):
                method_value = getattr(self, method_name)

                if callable(method_value):
                    bench_cases_methods.append((method_name, method_value))

        return bench_cases_methods

    @property
    def benchmarks(self):
        if not self._benchmarks:
            self._benchmarks = []
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

    def exec_benchmark(self, method_name, method_value, repeat=10):
        self.setUp()

        exec_times = [self.tick(method_value, self) for x in [0.0] * repeat]
        exec_stats = ExecutionStats(average=average(exec_times),
                                                  median=median(exec_times),
                                                  fastest=min(exec_times),
                                                  slowest=max(exec_times))

        self.results['times'].update({method_name: exec_times})
        self.results['stats'].update({method_name: exec_stats})

        self.tearDown()

        return exec_times, exec_stats

    def iter(self, sampling=10, *args, **kwargs):
        for method_name, method_value in self.benchmarks:
            exec_times, exec_stats = self.exec_benchmark(method_name,
                                                                                 method_value,
                                                                                 sampling)
            yield method_name, exec_times, exec_stats

    def run(self, sampling=10, *args, **kwargs):
        return self.formatter.apply(self.iter(sampling), self.__class__.__name__)


class BenchSuite(object):
    def __init__(self):
        self.benchcases = []

    def add_benchcase(self, benchcase):
        # if it walks like a duck, swims like a duck and quacks like a duck...
        if hasattr(benchcase, 'run') and benchcase.benchmarks:
            self.benchcases.append(benchcase)

    def run(self, *args, **kwargs):
        ran = 0

        for benchcase in self.benchcases:
            ran += benchcase.run(*args, **kwargs)

        return ran
