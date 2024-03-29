import functools
import inspect
import logging
import sys

from multitool import console


def wrap_with_exception_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error('Exception occurred', exc_info=True)
            frm = inspect.trace()[-1]
            mod = inspect.getmodule(frm[0])
            modname = mod.__name__ if mod else frm[1]
            sys.exit(f'An exception of type {modname}.{type(e).__name__} occurred. Arguments:\n{e}')
        except KeyboardInterrupt:
            console.echo()
            sys.exit(130)

    return wrapper
