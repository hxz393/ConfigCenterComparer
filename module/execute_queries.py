"""
这是一个用于处理数据库查询和结果格式化的Python模块。

此模块提供了主要的功能：执行针对不同环境的数据库查询，并将查询结果按照特定的格式处理。它支持通过配置中心的不同配置来处理不同环境下的数据库查询，并将查询结果格式化以便后续使用。

本模块的目的是为了提供一个高效、灵活的方法来处理跨环境的数据库查询和结果的格式化。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any, Tuple

from .format_query_results import format_query_results
from .get_query_result import get_query_result

logger = logging.getLogger(__name__)


def execute_queries(config_connection: Dict[str, Any], config_main: Dict[str, Any], query_sql: str) -> Tuple[Dict[str, Any], Dict[str, bool]]:
    """
    根据配置执行数据库查询，并处理查询结果。

    此函数遍历给定的数据库连接配置，对每个环境执行 SQL 查询，并收集查询结果。查询结果通过调用 `format_query_results` 函数进行格式化。函数返回格式化后的结果和每个环境的查询状态。

    :param config_connection: 包含数据库连接配置的字典，键为环境名称，值为对应的数据库配置。
    :type config_connection: Dict[str, Any]
    :param config_main: 包含主要配置信息的字典，用于查询结果的格式化。
    :type config_main: Dict[str, Any]
    :param query_sql: 要执行的 SQL 查询语句。
    :type query_sql: str
    :return: 一个包含格式化查询结果的字典和一个包含每个环境查询状态的字典。
    :rtype: Tuple[Dict[str, Any], Dict[str, bool]]
    """
    query_statuses = {env_name: False for env_name in config_connection.keys()}
    formatted_results = {}

    try:
        for env_name, db_config in config_connection.items():
            query_results = get_query_result(db_config, query_sql)
            if query_results:
                format_query_results(query_results, env_name, config_main, formatted_results)
                query_statuses[env_name] = True
            else:
                logger.warning(f"No results obtained from database query for environment: {env_name}")
        return formatted_results, query_statuses
    except Exception:
        logger.exception("Exception occurred during executing queries")
        return {}, {env_name: False for env_name in config_connection.keys()}
