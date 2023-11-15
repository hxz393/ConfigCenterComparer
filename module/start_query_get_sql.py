"""
这是一个用于数据库配置查询的Python模块。

此模块包含主要的函数 `get_query_sql`，用于根据不同的配置中心类型获取相应的SQL查询语句。支持的配置中心包括Nacos和Apollo。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Optional

from config.settings import SQL_CONFIG_APOLLO_ID, SQL_CONFIG_NACOS, SQL_CONFIG_APOLLO_NAME

logger = logging.getLogger(__name__)


def start_query_get_sql(config_main: Dict[str, str]) -> Optional[str]:
    """
    根据配置中心类型和Apollo名称获取相应的SQL查询语句。

    根据提供的配置中心类型（例如：Nacos或Apollo）和Apollo名称（例如：AppId或Name），
    返回相应的SQL查询语句。如果配置中心类型不支持或配置信息不完整，则返回None。

    :param config_main: 包含配置中心类型和Apollo名称的字典。
    :type config_main: Dict[str, str]
    :rtype: Optional[str]
    :return: 相应的SQL查询语句，如果配置不正确则返回 None。
    """
    config_center = config_main.get('config_center')
    apollo_name = config_main.get('apollo_name')

    try:
        if config_center == 'Nacos':
            return SQL_CONFIG_NACOS
        elif config_center == 'Apollo':
            if apollo_name == 'AppId':
                return SQL_CONFIG_APOLLO_ID
            elif apollo_name == 'Name':
                return SQL_CONFIG_APOLLO_NAME
        else:
            return None
    except Exception:
        logger.exception("Unexpected error when getting SQL")
        return None
