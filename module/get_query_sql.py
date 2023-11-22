"""
此模块用于处理配置中心相关的查询，包括从不同的配置中心获取 SQL 查询语句。

本模块提供了 `get_query_sql` 函数，用于根据配置中心类型和 Apollo 应用名称获取对应的查询 SQL。支持从 Nacos 和 Apollo 配置中心获取数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Optional

from config.settings import SQL_CONFIG_NACOS, SQL_CONFIG_APOLLO_ID, SQL_CONFIG_APOLLO_NAME, APOLLO_NAME_LIST

logger = logging.getLogger(__name__)


def get_query_sql(config_main: Dict[str, str]) -> Optional[str]:
    """
    根据配置中心类型和 Apollo 应用名称获取查询 SQL。

    此函数接收一个字典，包含配置中心类型和 Apollo 应用名称。它根据配置中心类型（Nacos 或 Apollo）以及 Apollo 应用名称（'AppId' 或 'Name'），返回相应的 SQL 查询语句。

    :param config_main: 包含配置中心类型和 Apollo 应用名称的字典。
    :type config_main: Dict[str, str]
    :return: 对应的查询 SQL 语句。如果无法匹配到合适的配置中心或应用名称，则返回 None。
    :rtype: Optional[str]

    :example:
    >>> get_query_sql({"config_center": "Nacos"})
    SQL_CONFIG_NACOS
    >>> get_query_sql({"config_center": "Apollo", "apollo_name": "AppId"})
    SQL_CONFIG_APOLLO_ID
    >>> get_query_sql({"config_center": "Apollo", "apollo_name": "Name"})
    SQL_CONFIG_APOLLO_NAME
    """
    try:
        config_center = config_main.get('config_center')
        apollo_name = config_main.get('apollo_name')

        if config_center == 'Nacos':
            return SQL_CONFIG_NACOS
        elif config_center == 'Apollo' and apollo_name in APOLLO_NAME_LIST:
            return SQL_CONFIG_APOLLO_ID if apollo_name == 'AppId' else SQL_CONFIG_APOLLO_NAME
        else:
            return None
    except Exception:
        logger.exception("Error retrieving query SQL")
        return None
