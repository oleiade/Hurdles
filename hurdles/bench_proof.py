import hurdles


class BenchRandom(hurdles.BenchCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def bench_random(self):
        l = [x for x in xrange(100000)]

    def bench_random_bis(self):
        l = [x for x in xrange(200000)]

    def bench_random_ter(self):
        l = [x for x in xrange(300000)]

if __name__ == "__main__":
    B = BenchRandom()
    B.run()
