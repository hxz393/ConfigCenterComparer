"""
这是一个用于合并和更新格式化结果的Python模块。

此模块提供了一个主要函数：`merge_formatted_results`，用于将新的结果字典合并到现有的结果字典中。此操作主要用于在数据处理中更新和整合来自不同来源的信息。

本模块的主要目的是提供一个简洁有效的方式来处理和更新复杂的字典结构数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from typing import Dict, Any

logger = logging.getLogger(__name__)


def merge_formatted_results(existing_results: Dict[str, Dict[str, Any]], new_result: Dict[str, Dict[str, Any]]) -> None:
    """
    合并现有结果与新的结果。

    此函数负责将新的结果字典合并到现有的结果字典中。如果已存在的键，则更新其值；如果不存在，则添加新的键值对。

    :param existing_results: 现有的结果字典，其中每个键对应一个字典结构的值。
    :type existing_results: Dict[str, Dict[str, Any]]
    :param new_result: 新的结果字典，其结构应与现有结果字典相同。
    :type new_result: Dict[str, Dict[str, Any]]
    """
    try:
        for key, value in new_result.items():
            existing_results.setdefault(key, {}).update(value)
    except Exception:
        logger.exception("Error occurred while merging formatted results.")
