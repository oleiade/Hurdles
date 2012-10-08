import sys

from hurdles.referee.actions import get_bench_from_cmdline, discover_benchmarks


def main():
    paths = get_bench_from_cmdline(sys.argv[1:])
    benchmarks = discover_benchmarks(paths)

    for bench in benchmarks:
        bench().run()

    sys.stdout.write('\n' + ('-' * 80) + '\n')
    sys.stdout.write('Done.\n')
