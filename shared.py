from functools import wraps
from time import perf_counter

def timer(func):
    @wraps(func)
    def wrapper(*arg):
        start = perf_counter()
        res = func(*arg)
        print(f"{func.__name__!r} took {(perf_counter() - start):.6f} seconds")
        return res

    return wrapper

