"""
此模块提供数据库查询功能，支持通过 SSH 进行 MySQL 查询。

本模块主要包含一个函数 `start_query_get_result`，用于根据提供的数据库配置和 SQL 查询语句，执行数据库查询。支持通过 SSH 隧道连接到 MySQL 数据库，以及直接连接到 MySQL 数据库的功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, Union

from lib.mysql_query import mysql_query
from lib.mysql_query_with_ssh import mysql_query_with_ssh

logger = logging.getLogger(__name__)


def start_query_get_result(db_config: dict, query_sql: str) -> Optional[Union[tuple, None]]:
    """
    根据数据库配置和 SQL 查询语句执行查询，并返回查询结果。

    此函数首先检查数据库配置是否开启了 MySQL 和 SSH，然后根据配置执行相应的查询函数。如果数据库未开启或者发生异常，将返回 None。

    :param db_config: 包含数据库配置信息的字典，应包含 MySQL 和 SSH 配置。
    :type db_config: dict
    :param query_sql: 要执行的 SQL 查询语句。
    :type query_sql: str
    :return: 查询成功时返回查询结果，如果数据库未开启或发生异常则返回 None。
    :rtype: Optional[Union[tuple, None]]
    """
    try:
        if not db_config.get('mysql_on'):
            return None

        if db_config.get('ssh_on'):
            return mysql_query_with_ssh(ssh_config=db_config['ssh'], mysql_config=db_config['mysql'], query_sql=query_sql)
        else:
            return mysql_query(mysql_config=db_config['mysql'], query_sql=query_sql)
    except Exception:
        logger.exception("Unexpected error during query execution")
        return None
