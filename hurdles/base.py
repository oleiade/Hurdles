# -*- coding:utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

import sys
import time

from collections import namedtuple
from inspect import getmembers, ismethod


ExecTimeCollection = namedtuple('ExecTimeCollection', ['times', 'scale'])


class InvalidBenchmarkError(Exception):
    pass


class BenchCase(object):
    def __init__(self, methods=None):
        self.results = {
            'exec_times': {},
            'averages': {},
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

        exec_times = ExecTimeCollection(times=[self.tick(method_value, self) for x in [0.0] * repeat],
                                        scale='ms')
        average = sum(exec_times.times) / repeat

        self.results['exec_times'].update({method_name: exec_times})
        self.results['averages'].update({method_name: average})

        self.tearDown()

        return exec_times, average

    def iter(self, sampling=10):
        for method_name, method_value in self.benchmarks:
            exec_times, average = self.exec_benchmark(method_name,
                                                      method_value,
                                                      sampling)
            yield method_name, exec_times, average

    def run(self, sampling=10):
        for method_name, exec_times, average in self.iter(sampling=sampling):
            ref_class = self.__class__.__name__

            sys.stdout.write("{0}.{1} ... {2} {3}\n".format(ref_class,
                                                            method_name,
                                                            average,
                                                            exec_times.scale))


# def BenchSuite(object):
#     def __init__(self):
#         self.bench_cases = []

#     def _register_benchcase(self, bench_case):
#         if hasattr(bench_case, 'run') and bench_case.benchmarks:
#             self.bench_cases.append(bench_cases)

#     def add(self, bench_cases):
#         for bench in bench_cases:
#             try:
#                 self.register(bench)
#             except InvalidBenchmarkError:
#                 continue

#     def run(self):
#         pass