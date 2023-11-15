"""
这是一个用于过滤特定结果的Python模块。

本模块主要包含一个函数 `apply_filter_to_results`，该函数用于将预先定义的过滤规则应用于给定的结果字典，以便根据特定条件排除或标记某些结果项。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict

from config import FILTER_PATH
from lib import read_file_to_list

logger = logging.getLogger(__name__)


def apply_filter_to_results(results: Dict[str, Dict[str, str]]) -> None:
    """
    应用过滤器到结果字典。

    此函数读取定义的过滤列表，并更新结果字典中的条目，为符合过滤条件的条目标记特定值。

    :param results: 结果字典，其中每个键对应一个结果项，且每个结果项是一个字典。
    :type results: Dict[str, Dict[str, str]]
    """
    try:
        # 读取过滤列表
        skip_list = read_file_to_list(FILTER_PATH) or []

        # 更新结果字典
        for index_key in results:
            results[index_key]['filter'] = '1' if index_key in skip_list else '0'
    except Exception:
        logger.exception("Error occurred while applying filter to results")
