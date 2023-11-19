"""
提供配置中心查询 SQL 的功能模块。

此模块包含主要函数 `get_query_sql`，用于根据配置中心类型和 Apollo 应用名称获取相应的查询 SQL 语句。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

from typing import Dict, Optional

from config.settings import SQL_CONFIG_NACOS, SQL_CONFIG_APOLLO_ID, SQL_CONFIG_APOLLO_NAME, APOLLO_NAME_LIST
import logging

logger = logging.getLogger(__name__)


def get_query_sql(config_main: Dict[str, str]) -> Optional[str]:
    """
    根据配置中心类型和 Apollo 应用名称获取查询 SQL。

    此函数根据提供的配置中心类型和 Apollo 应用名称，返回相应的 SQL 查询语句。支持的配置中心类型包括 'Nacos' 和 'Apollo'。对于 'Apollo'，进一步根据应用名称（'AppId' 或 'Name'）返回不同的 SQL 语句。

    :param config_main: 包含配置中心类型和 Apollo 应用名称的字典。
    :type config_main: Dict[str, str]
    :return: 对应的查询 SQL 语句，如果无法获取则返回 None。
    :rtype: Optional[str]
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
