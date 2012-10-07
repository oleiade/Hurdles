## Overview

A simple and yet powerful python benchmark framework. Write unit benchs just like you'd write unit tests.

*It's not only about crossing the finish line, it's about finding the hurdles that to slow you down*

## Usage

Just like you'd write unittest, subclass the BenchCase class, and there you go.

```python
import hurdles

class BenchMyClass(hurdles.BenchCase):
    def setUp(self):
        # Just like when unit testing
        # Set up some attributes here
        # that will be set up in each bench

    def tearDown(self):
        # Once again, just like unit testing
        # get rid of what you've set up and want
        # to be reset between each benchmark

    # Every benchmark method has to start with 'bench_'
    # to be run as a benchmark by hurdles
    def bench_this(self, *args, **kwargs):
        # Do some stuff that you'd wanna time here
        return [random.randint(1, 100000) for x in [0] * 100000]

    def bench_that(self, *args, **kwargs):
        return [random.randint(1, 10000) for x in [0] * 10000]

if __name__ == "__main__":
    B = BenchCase()
    B.run()
```

Run it `python mybench.py`
and enjoy the results:

```bash
BenchMyClass.bench_this ... X ms
BenchMyClass.bench_that ... Y ms
```

*For more examples, see `examples` included folder*