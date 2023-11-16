"""
这是一个用于处理和格式化配置中心查询结果的Python模块。

此模块提供了主要的功能：处理查询结果并将其格式化为特定结构的字典，主要用于不同配置中心（如Apollo和Nacos）的数据处理。它提供了将查询结果从原始格式转换为更易于理解和处理的格式化字典的能力。

本模块的主要目的是为了提高处理来自不同配置中心的数据的效率，并保持数据格式的一致性。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any, Tuple

from .format_single_query_result import format_single_query_result
from .merge_formatted_results import merge_formatted_results

logger = logging.getLogger(__name__)


def format_query_results(query_results: Tuple[Tuple[str, Any]], env_name: str, name_config: Dict[str, Any], formatted_results: Dict[str, Dict[str, Any]]) -> None:
    """
    根据配置中心类型和环境名称，处理多个查询结果并将其合并到已有的结果字典中。

    此函数接受多个查询结果，针对每个结果调用 `format_single_query_result` 函数进行格式化，然后将格式化后的结果合并到一个统一的字典中。这有助于统一管理来自不同源的配置数据。

    :param query_results: 包含多个查询结果的元组，每个结果包括应用名、命名空间和其它数据。
    :type query_results: Tuple[Tuple[str, Any]]
    :param env_name: 环境名称，用于确定格式化的上下文。
    :type env_name: str
    :param name_config: 包含配置中心类型和其它相关配置的字典。
    :type name_config: Dict[str, Any]
    :param formatted_results: 已格式化的结果字典，用于合并新的格式化结果。
    :type formatted_results: Dict[str, Dict[str, Any]]
    """
    try:
        for single_query_result in query_results:
            formatted_result = format_single_query_result(single_query_result, env_name, name_config)
            if formatted_result:
                merge_formatted_results(formatted_results, formatted_result)
    except Exception:
        logger.exception("Unexpected error during formatting query results")
