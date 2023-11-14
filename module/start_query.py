"""
这是一个用于执行数据库查询并处理结果的模块。

本模块提供了 `start_query` 函数，用于在多个环境中执行 SQL 查询，并根据指定配置处理查询结果。
它支持通过 SSH 连接到数据库，并能够对查询结果进行格式化处理。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any, Optional

from lib.mysql_query import mysql_query
from lib.mysql_query_with_ssh import mysql_query_with_ssh
from .start_query_get_sql import start_query_get_sql
from .start_query_result_format import start_query_result_format

# 初始化日志记录器
logger = logging.getLogger(__name__)


def start_query(config_connection: Dict[str, Any], config_main: Dict[str, Any]) -> Optional[Dict[str, Dict[str, Any]]]:
    """
    在多个环境中执行 SQL 查询并处理结果。

    此函数接受数据库连接配置和主配置，针对每个环境执行 SQL 查询并格式化结果。
    支持通过 SSH 连接到数据库。

    :param config_connection: 包含每个环境数据库连接配置的字典。
    :type config_connection: Dict[str, Any]
    :param config_main: 包含主配置的字典。
    :type config_main: Dict[str, Any]
    :return: 各环境查询结果的字典。
    :rtype: Optional[Dict[str, Dict[str, Any]]]
    """
    try:
        result_dict = {}

        query_sql = start_query_get_sql(config_main)
        if not query_sql:
            return None

        for env_name, config in config_connection.items():
            if not config.get('mysql_on'):
                continue

            if config.get('ssh_on'):
                query_result = mysql_query_with_ssh(ssh_config=config['ssh'], mysql_config=config['mysql'], query_sql=query_sql)
            else:
                query_result = mysql_query(mysql_config=config['mysql'], query_sql=query_sql)
            if not query_result:
                logger.warning(f"No results obtained from database query for environment: {env_name}")
                continue

            for query_result_one in query_result:
                result_dict = start_query_result_format(query_result_one, env_name, config_main, result_dict)
                if not result_dict:
                    logger.error(f"Error formatting query result for environment: {env_name}, Data: {query_result_one}")
                    continue

        return result_dict

    except Exception:
        logger.exception(f'Error occurred during execution')
        return None
