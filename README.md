## Overview

A simple and yet powerful python benchmark framework. Write unit benchs just like you'd write unit tests.

*It's not only about crossing the finish line, it's about finding the hurdles that to slow you down*

## Usage


### Writing Bench cases

Just like you'd write unittest, subclass the BenchCase class, and there you go.

**Nota** : hurdles will only consider file named following the pattern 'bench_*.py'
and will only run against Bench classes which name starts with 'Bench'


```python
from hurdles import BenchCase
from hurdles.tools import extra_setup


from hurdles.tools import extra_setup

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
        return [x for x in [0] * 100000]

    # hurdles.tools provides an extra_setup decorator
    # which provides the ability to run some setup code
    # outside the timed benchmark running, in order
    # to prepare some data, import some dependencies etc...
    # Once prepared, context is injected into kwargs.
    @extra_setup("from random import randint"
                 "r = [x for x in xrange(10000)]")
    def bench_that(self, *args, **kwargs):
        [randint(0, 1000) for x in kwargs['r']]
```

### Running bench cases

##### Via Code
>>>>>>> devel

Running bench cases benchmarks can be made via the .run or .iter method. You can restrain benchmarks
methods to be run at a BenchCase instanciation.

```python
    B = BenchMyClass()  # will run every BenchMyClass benchmarks
    # or
    B = BenchMyClass(['bench_this'])  # will only run BenchMyClass 'bench_this' method

    # BenchCase class provides a .run method to run and print
    # on stdout benchmarks results.
    B.run()

    # and a .iter method which provides an iterator over benchmarks
    # methods.
    it = B.iter()
    [do_some_stuff(b) for b in it]
```

<<<<<<< HEAD
#### From python

Or, you can eventually run your bench classes by yourself calling the run method over your classes:
=======
Just like unittest lib provides test cases suites, hurdles comes with bench cases suites.
>>>>>>> devel

```python
suite = BenchSuite()
suite.add_benchcase(BenchMyCase())
suite.add_benchcase(BenchMyOtherCase(['bench_foo', 'bench_bar'])

suite.run()
```

##### Via Cmdline

Hurdles comes with a cmdline util to run your bench cases :

```bash
$ hurdles mybenchmarksfolder1/ mybenchmarksfolder2/ benchmarkfile1
```

Which will auto-detect your benchmark modules, and classes, and run them (uses a BenchSuite under the hood).
the results should output on stdout like the following :

```bash
BenchMyClass.bench_this ... X ms
BenchMyClass.bench_that ... Y ms
--------------------------------
Done.
```

*For more examples, see `examples` included folder*