import random

import hurdles


class BenchRandom(hurdles.BenchCase):
    def bench_this(self):
        return [random.randint(1, 100000) for x in [0] * 100000]

    def bench_that(self):
        return [random.randint(1, 10000) for y in [0] * 10000]

if __name__ == "__main__":
    B = BenchRandom()
    B.run()
