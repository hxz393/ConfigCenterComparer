"""
此模块提供了对查询结果进行格式化处理的功能。它支持不同配置中心的查询结果格式化，并合并处理后的结果。

主要功能包括格式化Apollo和Nacos配置中心的查询结果，并将这些结果合并到一个字典中。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import datetime
import logging
from typing import Dict, Tuple, Union

from module.format_apollo_result import format_apollo_result
from module.format_nacos_result import format_nacos_result
from module.merge_formatted_results import merge_formatted_results
from module.modify_name import modify_name

logger = logging.getLogger(__name__)


def format_query_results(
        query_results: Union[Tuple[Tuple[str, str, str, str, datetime.datetime], ...], Tuple[Tuple[str, str, str, datetime.datetime], ...]],
        env_name: str,
        config_main: Dict[str, str],
        formatted_results: Dict[str, Dict[str, str]]
) -> None:
    """
    格式化查询结果，并根据不同的配置中心处理它们。

    此函数处理Apollo和Nacos配置中心的查询结果。它使用 modify_name 函数来处理名称字段，并根据配置中心的类型调用相应的格式化函数。

    :param query_results: 查询结果，可能是多种不同格式的元组或None。
    :type query_results: QueryResult
    :param env_name: 环境名称。
    :type env_name: str
    :param config_main: 主要配置参数字典。
    :type config_main: Dict[str, str]
    :param formatted_results: 格式化后的结果将被存储的字典。
    :type formatted_results: Dict[str, Dict[str, str]]
    :return: None
    :rtype: None

    :example:
    >>> results = (('admin', 'application', 'resource.search.debugEnabled', 'true', datetime.datetime(2022, 8, 1, 11, 41, 44)), ('basic', 'application', 'spring.application.name', 'basic', datetime.datetime(2023, 10, 31, 13, 37, 43)),)
    >>> env = "PRO_CONFIG"
    >>> config = {"config_center": "Apollo", 'apollo_name': 'AppId', "fix_name_left": "app-", "fix_name_right": "-test", "fix_name_before": "old", "fix_name_after": "new"}
    >>> f_results = {}
    >>> format_query_results(results, env, config, f_results)
    >>> print(f_results)
    {'admin+application+resource.search.debugEnabled': {'app_id': 'admin', 'namespace_name': 'application', 'key': 'resource.search.debugEnabled', 'PRO_CONFIG': 'true', 'PRO_CONFIG_modified_time': '2022-08-01 11:41:44'}, 'basic+application+spring.application.name': {'app_id': 'basic', 'namespace_name': 'application', 'key': 'spring.application.name', 'PRO_CONFIG': 'basic', 'PRO_CONFIG_modified_time': '2023-10-31 13:37:43'}}
    """
    try:
        # 简化变量分配
        prefixes = config_main['fix_name_left'].split()
        suffixes = config_main['fix_name_right'].split()
        replacements = dict(zip(config_main['fix_name_before'].split(), config_main['fix_name_after'].split()))

        for single_query_result in query_results:
            name, namespace_name, *rest = single_query_result
            # 处理app_id字段
            app_id = modify_name(name, prefixes, suffixes, replacements)

            # 根据不同配置中心，格式化查询结果
            if config_main['config_center'] == 'Apollo':
                # 返回只有一个键值对的字典
                formatted_result = format_apollo_result(app_id, namespace_name, rest, env_name)
            else:
                # 返回有多个键值对的字典
                formatted_result = format_nacos_result(app_id, namespace_name, rest, env_name)

            if formatted_result:
                # 合并单条格式化字典到总字典
                merge_formatted_results(formatted_results, formatted_result)
            else:
                logger.error(f'Formatting error for result: {single_query_result}')

    except Exception:
        logger.exception(f"Unexpected error during formatting query results. ENV name: {env_name}")
