import random

import hurdles

from hurdles.tools import extra_setup


class BenchRandom(hurdles.BenchCase):
    @extra_setup("""import random""")
    def bench_this(self, *args, **kwargs):
        return [random.randint(1, 100000) for x in [0] * 100000]

    def bench_that(self, *args, **kwargs):
        return [random.randint(1, 10000) for y in [0] * 10000]

if __name__ == "__main__":
    B = BenchRandom()
    B.run()
