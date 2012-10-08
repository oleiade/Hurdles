from functools import wraps


def extra_setup(setup_code):
    """Allows to setup some extra context to it's decorated function.

    As a convention, the bench decorated function should always handle
    *args and **kwargs. Kwargs will be updated with the extra context
    set by the decorator.

    Example:
        @extra_setup("l = [x for x in xrange(100)]")
        def bench_len(self, *args, **kwargs):
            print len(kwargs['l'])
    """
    def decorator(func):
        # Exec extra setup code and put it in a local
        # context passed to function through kwargs.
        context = {}
        exec setup_code in {}, context

        @wraps(func)
        def decorated_function(*args, **kwargs):
            kwargs.update(context)
            return func(*args, **kwargs)
        return decorated_function
    return decorator
