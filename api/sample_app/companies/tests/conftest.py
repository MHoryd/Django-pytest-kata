from typing import Callable
from datetime import datetime, timedelta


class PerformanceException(Exception):
    def __init__(self, runtime: timedelta, limit: timedelta):
        self.runtime = runtime
        self.limit = limit

    def __str__(self) -> str:
        return f"Performance test failed, runtime: {self.runtime.total_seconds()}, limit: {self.limit.total_seconds()}"


def check_performance(function: Callable, runtime_limit=timedelta(seconds=2)):

    def run_function_and_validate_runtime(*args, **kwargs):
        start = datetime.now()
        result = function(*args, **kwargs)
        end = datetime.now()
        runtime = end - start
        print(f"Runtime for function was: {runtime.total_seconds()}")
        if runtime > runtime_limit:
            raise PerformanceException(runtime=runtime, limit=runtime_limit)

        return result

    return run_function_and_validate_runtime
