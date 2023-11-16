"""
这是一个用于数据库查询和配置管理的Python模块。

此模块主要包含 `start_query` 函数，用于连接数据库并根据配置执行查询。它会调用多个辅助函数来处理查询结果，包括获取查询SQL、执行查询、更新配置一致性状态和跳过状态。

本模块的目的是提供一个统一的入口点，用于执行配置中心的数据查询并处理结果。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any, Optional, List

from .execute_queries import execute_queries
from .get_query_sql import get_query_sql
from .update_config_consistency_status import update_config_consistency_status
from .update_config_skip_status import update_config_skip_status

logger = logging.getLogger(__name__)


def start_query(config_connection: Dict[str, Any], config_main: Dict[str, Any]) -> Optional[List[Any]]:
    """
    启动查询过程，使用给定的配置连接数据库并执行查询。

    此函数首先通过 `get_query_sql` 获取查询SQL，然后使用 `execute_queries` 执行查询。查询结果通过 `update_config_consistency_status` 和 `update_config_skip_status` 函数处理，最终返回一个包含查询结果和查询状态的列表。

    :param config_connection: 数据库连接配置字典。
    :type config_connection: Dict[str, Any]
    :param config_main: 主配置字典。
    :type config_main: Dict[str, Any]
    :return: 包含查询结果和查询状态的列表，如果发生异常则返回 None。
    :rtype: Optional[List[Any]]
    """
    try:
        # 获取数据库查询语句
        query_sql = get_query_sql(config_main)
        if not query_sql:
            logger.error("Error getting query SQL")
            return None

        # 获取数据库查询结果
        formatted_results, query_statuses = execute_queries(config_connection, config_main, query_sql)
        if not formatted_results:
            logger.error("Error in querying databases")
            return None

        # 查询各配置环境的值，得到一致性信息，更新到结果字典
        update_config_consistency_status(formatted_results, query_statuses)

        # 通过对比过滤列表，得到是否过滤信息，更新到结果字典
        update_config_skip_status(formatted_results)

        return [formatted_results, query_statuses]
    except Exception:
        logger.exception('Error occurred during execution')
        return None
