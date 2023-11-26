"""
此模块提供了日志记录和时间测量功能，用于监控和调试软件应用程序。

本模块包含一个装饰器函数 `log_time`，该函数可以记录被装饰函数的执行时间。这对于性能分析和优化非常有用。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import time
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def log_time(func: Callable) -> Callable:
    """
    一个装饰器，用于记录被装饰函数的运行时间。

    此装饰器在函数执行前后记录时间，计算并记录函数的运行时间。如果函数执行期间出现异常，将记录异常并返回 None。

    :param func: 被装饰的函数。
    :type func: Callable
    :return: 包装后的函数。
    :rtype: Callable

    :example:
    >>> @log_time
    ... def test_function():
    ...     time.sleep(1)
    ...
    >>> test_function()  # 这将记录 test_function 的运行时间
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """
        包装函数，用于实际执行被装饰的函数并计算其运行时间。

        此函数首先记录开始时间，然后尝试执行原始函数，最后记录结束时间并计算运行时长。如果在执行过程中出现异常，会记录异常信息。

        :param args: 原始函数的位置参数。
        :param kwargs: 原始函数的关键字参数。
        :return: 原始函数的返回值，如果出现异常则返回 None。
        :rtype: Any
        """
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception occurred in {func.__name__}: {e}")
            return None
        else:
            end_time = time.time()
            logger.debug(f"{func.__name__} executed in {end_time - start_time:.2f} seconds.")
            return result

    return wrapper
