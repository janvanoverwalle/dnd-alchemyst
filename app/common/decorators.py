import functools
import pytest


def raises(ex):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with pytest.raises(ex):
                return func(*args, **kwargs)
        return wrapper
    return decorator
