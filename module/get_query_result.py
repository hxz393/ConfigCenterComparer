"""
这是一个用于数据库查询和处理的Python模块。

此模块提供了主要函数 `get_query_result`，用于根据提供的数据库配置和SQL语句执行查询操作。此函数支持通过SSH进行远程查询，以及直接连接到MySQL数据库进行查询。

本模块的主要目的是提供一个简单有效的方式来执行数据库查询，并处理可能的异常情况。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, Dict, Any, Tuple

from lib.mysql_query import mysql_query
from lib.mysql_query_with_ssh import mysql_query_with_ssh

logger = logging.getLogger(__name__)


def get_query_result(db_config: Dict[str, Any], query_sql: str) -> Optional[Tuple[Tuple[Any, ...], ...]]:
    """
    根据数据库配置执行 SQL 查询。

    此函数根据提供的数据库配置执行 SQL 查询。如果配置中包含 'ssh_on' 选项，将通过 SSH 进行远程查询；否则，直接连接到 MySQL 数据库。

    :param db_config: 包含数据库连接参数的字典。可能包括 SSH 配置。
    :type db_config: Dict[str, Any]
    :param query_sql: 要执行的 SQL 查询语句。
    :type query_sql: str
    :return: 查询结果的元组，如果出现异常或配置中 'mysql_on' 为 False 则返回 None。
    :rtype: Optional[Tuple[Tuple[Any, ...], ...]]
    """
    try:
        if not db_config.get('mysql_on'):
            return None

        if db_config.get('ssh_on'):
            return mysql_query_with_ssh(ssh_config=db_config['ssh'], mysql_config=db_config['mysql'], query_sql=query_sql)
        else:
            return mysql_query(mysql_config=db_config['mysql'], query_sql=query_sql)
    except Exception as e:
        logger.exception(f"Error executing query: {e}")
        return None
