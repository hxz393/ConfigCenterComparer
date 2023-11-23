"""
这个模块提供了用于合并格式化结果的功能，可以将新的格式化结果字典合并到一个已有的格式化结果字典中。

主要功能是 `merge_formatted_results` 函数，它处理字典类型的数据，将新的字典内容合并到既定的字典中。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


def merge_formatted_results(
        formatted_results: Dict[str, Dict[str, str]],
        formatted_result: Dict[str, Dict[str, str]]
) -> None:
    """
    将新的格式化结果字典合并到已有的格式化结果字典中。

    此函数接收两个参数：一个存储已有格式化结果的字典和一个新的格式化结果字典。它会遍历新字典的每个项，并将其内容合并到已有字典的相应项中。

    :param formatted_results: 存储已有格式化结果的字典。
    :type formatted_results: Dict[str, Dict[str, str]]
    :param formatted_result: 新的格式化结果字典，将被合并到 formatted_results 中。
    :type formatted_result: Dict[str, Dict[str, str]]
    :return: 无返回值。
    :rtype: None

    :example:
    >>> existing_results = {"index_key1": {"key1": "value1"}}
    >>> new_result = {"index_key1": {"key2": "value2"}, "index_key2": {"key3": "value3"}}
    >>> merge_formatted_results(existing_results, new_result)
    >>> print(existing_results)
    {'index_key1': {'key1': 'value1', 'key2': 'value2'}, 'index_key2': {'key3': 'value3'}}
    """
    """
    合并格式化结果。

    :type formatted_results: Dict[str, Dict[str, str]]
    :param formatted_results: 存储已有格式化结果的字典。
    :type formatted_result: Dict[str, Dict[str, str]]
    :param formatted_result: 新的格式化结果字典，将被合并到 formatted_results 中。
    """
    try:
        # 合并字典
        for index_key, config_dict in formatted_result.items():
            formatted_results.setdefault(index_key, {}).update(config_dict)
    except Exception:
        logger.exception("Error occurred while merging formatted results.")
