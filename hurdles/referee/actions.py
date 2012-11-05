import os
import inspect

from hurdles.referee.importer import *

is_bench_file = lambda filepath: bool(filepath.startswith('bench_') and filepath.endswith('.py'))
drop_file_ext = lambda filename: filename


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


def discover_benchmarks(benchmark_files):
    I = Importer()
    benchmarks = []

    for path in benchmark_files:
        mod_path, extension = os.path.splitext(path)
        mod_path, mod_filename = os.path.split(mod_path)

        module = I.importFromDir(mod_path, mod_filename)
        module_classes = inspect.getmembers(module, predicate=inspect.isclass)
        benchmarks.extend([klass[1] for klass
                           in module_classes
                           if klass[0].startswith('Bench')])

    return benchmarks
