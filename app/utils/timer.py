"""
timer.py

Simple execution timer.
"""

import time
from contextlib import contextmanager

from app.utils.logger import get_logger


logger = get_logger("timer")


@contextmanager
def timer(name: str):

    start = time.perf_counter()

    try:

        yield

    finally:

        elapsed = time.perf_counter() - start

        logger.info(
            f"{name} finished in {elapsed:.2f}s"
        )