# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

import os
import inspect

from hurdles.referee.importer import *

drop_file_ext = lambda filename: filename


def is_bench_file(filepath):
    if '/' in filepath:
        filepath = filepath.split('/')[-1]
    return bool(filepath.startswith('bench_') and filepath.endswith('.py'))


def get_bench_from_cmdline(cmdline):
    benchmark_files = []

    for path in cmdline:
        if os.path.exists(path):
            if os.path.isfile(path) and is_bench_file(path):
                benchmark_files.append(path)
            elif os.path.isdir(path):
                for path, dirs, files in os.walk(path):
                    for f in files:
                        if is_bench_file(f):
                            file_abspath = os.path.abspath(os.path.join(path, f))
                            benchmark_files.append(file_abspath)
            else:
                continue

    return benchmark_files


def discover_benchcases(benchcases_files):
    I = Importer()
    benchmarks = []

    for path in benchcases_files:
        mod_path, extension = os.path.splitext(path)
        mod_path, mod_filename = os.path.split(mod_path)

        module = I.importFromDir(mod_path, mod_filename)
        module_classes = inspect.getmembers(module, predicate=inspect.isclass)
        benchmarks.extend([klass[1] for klass
                           in module_classes
                           if klass[0].startswith('Bench')])

    return benchmarks
