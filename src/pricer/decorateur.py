import time
import logging
from functools import wraps

def timer(func):
    @wraps(func)  # preserves original function name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logging.info(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

@timer
def rebalance(w_current, w_target):
    return 'Calculating rebalance...'
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(rebalance(0.3, 0.5))
