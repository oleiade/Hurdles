## Overview

A simple and yet powerful python benchmark framework. Write unit benchs just like you'd write unit tests.

*It's not only about crossing the finish line, it's about finding the hurdles that to slow you down*

## Usage


### Writing Bench cases

Just like you'd write unittest, subclass the BenchCase class, and there you go.

**Nota** : Just like nose tool, hurdles will only consider file named following the pattern 'bench_*.py'
and will only run against Bench classes which name starts with 'Bench'


```python
from hurdles import BenchCase
from hurdles.tools import extra_setup


class BenchMyClass(BenchCase):
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

    # You can even set up some context for your benchmark
    # using the extra_setup decorator (it's generation won't be
    # considered while timing your methods execution time).
    # It's code will be compiled, executed, and the resulting locals
    # will be writen to kwargs.
    @extra_setup("import random"
                 "rands = [random.randint(1, 10000) for x in [0] * 10000]")
    def bench_that(self, *args, **kwargs):
        for r in kwargs['rands']:
            print r
```

### Running bench cases

#### From cmdline

To run your bench cases, you can whether use the shipped hurdles cmdline tool:

```bash
$ hurdles mybenchmarksfolder1/ mybenchmarksfolder2/ benchmarkfile1
```

Which will auto-detect your benchmark modules, and classes, and run them. 

#### From python

Or, you can eventually run your bench classes by yourself calling the run method over your classes:

```python
if __name__ == "__main__":
    B = BenchMyClass()
    B.run()
```

### Output

In every case, the results should output on stdout like this:

```bash
BenchMyClass.bench_this ... X ms
BenchMyClass.bench_that ... Y ms
--------------------------------
Done.
```

*For more examples, see `examples` included folder*