"""
该模块提供了数据库查询执行功能，包括执行查询、格式化查询结果和更新查询状态。

本模块包含 `execute_queries` 函数，用于执行数据库查询并处理结果。此外，还包括与查询结果格式化、状态更新相关的辅助函数。该模块适用于需要执行跨多个数据库环境的统一查询和结果处理的场景。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict, Tuple, Union

from module.format_query_results import format_query_results
from module.get_query_result import get_query_result
from module.get_query_sql import get_query_sql
from module.update_consistency_status import update_consistency_status
from module.update_skip_status import update_skip_status

logger = logging.getLogger(__name__)


def execute_queries(config_connection: Dict[str, Dict[str, Union[Dict[str, str], bool]]],
                    config_main: Dict[str, str]) -> Tuple[Dict[str, Dict[str, str]], Dict[str, bool]]:
    """
    执行数据库查询并返回格式化后的结果和查询状态。

    此函数接收数据库连接配置和主要配置参数。它首先根据主配置生成SQL查询语句，然后对每个数据库环境执行查询。查询结果将被格式化，并更新查询状态。

    :param config_connection: 数据库连接配置，包含环境名称和对应的数据库配置。
    :type config_connection: Dict[str, Dict[str, Union[Dict[str, str], bool]]]
    :param config_main: 主要配置参数，用于生成查询SQL语句。
    :type config_main: Dict[str, str]
    :return: 包含格式化查询结果的字典和每个环境的查询状态。
    :rtype: Tuple[Dict[str, Dict[str, str]], Dict[str, bool]]

    :example:
    >>> os.chdir(os.path.dirname(os.getcwd()))
    >>> connection = {"dev": {'mysql_on': True, 'ssh_on': False, 'mysql': {'host': '192.168.2.204', "port": "3306", "user": "root", "password": "QeqAr:%R+s5:hYnr", "db": "ApolloConfigDB_dev"}}}
    >>> main = {'config_center': 'Apollo', 'apollo_name': 'AppId', 'fix_name_before': '', 'fix_name_after': '', 'fix_name_left': '', 'fix_name_right': '',}
    >>> results, statuses = execute_queries(connection, main)
    >>> assert type(results) == dict
    >>> assert type(statuses) == dict
    >>> statuses
    >>> results
    """
    query_statuses = {env_name: False for env_name in config_connection.keys()}
    formatted_results = {}

    try:
        query_sql = get_query_sql(config_main)

        for env_name, db_config in config_connection.items():
            # 获取指定环境的查询结果
            query_results = get_query_result(db_config, query_sql)
            logger.debug(f"ENV: {env_name}, SQL query finished.")
            if query_results:
                query_statuses[env_name] = True
                # 格式化查询结果
                format_query_results(query_results, env_name, config_main, formatted_results)
            else:
                logger.warning(f"No results obtained from database query for environment: {env_name}")

        # 通过对比过滤列表，得到是否过滤信息，更新到结果字典
        update_skip_status(formatted_results)
        # 查询各配置环境的值，得到一致性信息，更新到结果字典。只对比查询成功的环境
        update_consistency_status(formatted_results, query_statuses)
        logger.debug("Status update finished.")

        return formatted_results, query_statuses
    except Exception:
        logger.exception("Exception occurred during executing queries")
        return {}, query_statuses
