"""
这是一个Python文件，包含用于执行 MySQL 查询并返回结果的函数 `mysql_query`。

函数 `mysql_query` 旨在接收数据库连接参数和一个 SQL 查询语句，它首先验证连接参数是否齐全且有效。如果验证通过，函数尝试连接到 MySQL 数据库，并执行提供的 SQL 查询语句。查询成功，它将返回结果集；如果遇到任何问题，例如连接失败或查询执行错误，函数将记录详细的错误信息并返回 None。

该模块是数据库操作的核心工具，提供了执行查询和处理结果的基础功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Any, Optional, Dict

import pymysql

# 初始化日志记录器
logger = logging.getLogger(__name__)


def mysql_query(mysql_config: Dict[str, Any], query_sql: str) -> Optional[tuple[tuple[Any, ...], ...]]:
    """
    执行 MySQL 查询并返回结果。

    :type mysql_config: Dict[str, Any]
    :param mysql_config: 包含MySQL数据库连接参数的字典。例如：{'host': '127.0.0.1', 'port': '3306', 'user': 'root', 'password': '123456', 'db': 'mysql'}
    :param query_sql: 要执行的 SQL 查询语句。
    :type query_sql: str
    :rtype:  Optional[tuple[tuple[Any, ...], ...]]
    :return: 查询结果的列表，如果发生异常则返回 None。
    """
    required_keys = ['host', 'port', 'user', 'password', 'db']
    if not all(key in mysql_config for key in required_keys):
        logger.error(f"MySQL configuration keys are missing.")
        return None

    if not all(mysql_config[key] for key in required_keys):
        logger.error(f"MySQL configuration contains empty values.")
        return None

    try:
        mysql_config['port'] = int(mysql_config['port'])
        with pymysql.connect(**mysql_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_sql)
                result = cursor.fetchall()
                return result
    except Exception:
        logger.exception(f"Unexpected error")
        return None
