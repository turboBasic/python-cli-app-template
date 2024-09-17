"""
Module for calculation of Fibonacci sequence
"""

import logging


def fibonacci(n: int) -> int:
    """Fibonacci example function"""
    logging.getLogger(__name__).debug('In fibonacci()')
    if not n > 0:
        message = f'{n} must be larger than 0!'
        raise RuntimeError(message)
    a, b = 1, 1
    for __ in range(n - 1):
        a, b = b, a + b
    return a
