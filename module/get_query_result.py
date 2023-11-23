"""
本模块包含用于数据库查询的函数，支持通过SSH进行MySQL查询。

主要包含 `get_query_result` 函数，用于根据数据库配置和SQL查询语句获取查询结果。
支持直接查询和通过SSH隧道查询两种方式。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import datetime
import logging
from typing import Dict, Tuple, Union

from lib.mysql_query import mysql_query
from lib.mysql_query_with_ssh import mysql_query_with_ssh

logger = logging.getLogger(__name__)


def get_query_result(
        db_config: Dict[str, Union[bool, Dict[str, str]]],
        query_sql: str
) -> Union[
    Tuple[Tuple[str, str, str, str, datetime.datetime], ...],
    Tuple[Tuple[str, str, str, datetime.datetime], ...],
    None
]:
    """
    根据数据库配置和SQL查询语句，获取查询结果。

    该函数根据提供的数据库配置执行SQL查询。如果配置中包含SSH设置，则通过SSH隧道进行查询。

    :param db_config: 包含数据库配置的字典，可能包含SSH配置。
    :type db_config: Dict[str, Union[bool, Dict[str, str]]]
    :param query_sql: 要执行的SQL查询语句。
    :type query_sql: str
    :return: 查询结果，可能是元组的元组，每个内部元组代表一行结果；或者为None。
    :rtype: QueryResult

    :example:
    >>> config = {'mysql_on': True, 'ssh_on': False, 'mysql': {'host': '192.168.2.204', "port": "3306", "user": "root", "password": "QeqAr:%R+s5:hYnr", "db": "ApolloConfigDB_dev"}}
    >>> sql = "SELECT n.AppId, n.NamespaceName, i.`Key`, i.`Value`, i.DataChange_LastTime FROM Item i INNER JOIN Namespace n ON i.NamespaceId = n.Id WHERE i.IsDeleted = 0 AND i.`Key` != '';"
    >>> get_query_result(config, sql)
    """
    try:
        if not db_config.get('mysql_on', False):
            return None

        if db_config.get('ssh_on', False):
            return mysql_query_with_ssh(ssh_config=db_config['ssh'], mysql_config=db_config['mysql'], query_sql=query_sql)
        else:
            return mysql_query(mysql_config=db_config['mysql'], query_sql=query_sql)
    except Exception:
        logger.exception(f"Error executing query MySQL with SQL: {query_sql}.")
        return None
