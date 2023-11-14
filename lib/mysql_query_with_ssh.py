"""
这个Python文件提供了一种通过SSH隧道连接到MySQL数据库并执行查询的方法。

它定义了一个主要函数 `mysql_query_with_ssh`，该函数接受SSH配置和MySQL配置参数，然后通过SSH隧道执行MySQL查询。这种方法对于访问位于防火墙或其他安全环境后面的数据库非常有用。

此模块的核心功能是通过SSH隧道进行安全的数据库查询，它对于需要通过加密连接访问数据库的场景特别重要。它使用了 `paramiko` 和 `sshtunnel` 库来建立SSH连接，并利用 `lib.mysql_query` 来执行实际的SQL查询。

在使用此模块时，用户需要提供SSH连接的详细信息（如主机名、端口、用户名和密码）以及MySQL数据库的连接参数（如主机、端口、用户名、密码和数据库名）。如果任何配置不完整或查询过程中发生错误，函数将记录相应的错误信息，并返回 `None`。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import traceback
from typing import Optional, Dict, Any

import paramiko
from paramiko import SSHClient
from sshtunnel import open_tunnel

from .mysql_query import mysql_query

# 初始化日志记录器
logger = logging.getLogger(__name__)
# 调整 Paramiko 的日志记录级别
logging.getLogger("paramiko").setLevel(logging.WARNING)


def mysql_query_with_ssh(ssh_config: Dict[str, Any], mysql_config: Dict[str, Any], query_sql: str) -> Optional[Any]:
    """
    通过SSH隧道执行MySQL查询。

    :param ssh_config: 包含 SSH 连接所需配置的字典。例如：{'hostname': '127.0.0.1', 'port': '22', 'username': 'root', 'password': 'abc123'}
    :type ssh_config: Dict[str, Any]

    :type mysql_config: Dict[str, Any]
    :param mysql_config: 包含MySQL数据库连接参数的字典。例如：{'host': '127.0.0.1', 'port': '3306', 'user': 'root', 'password': '123456', 'db': 'mysql'}
    :type query_sql: str
    :rtype: Optional[Any]
    :return: 查询结果或在发生错误时返回None。
    """
    required_keys_mysql = ['host', 'port', 'user', 'password', 'db']
    required_keys_ssh = ['hostname', 'port', 'username', 'password']

    if not all(key in ssh_config and ssh_config[key] for key in required_keys_ssh):
        logger.error(f"SSH configuration keys are missing or contain empty values: {ssh_config}")
        return None

    if not all(key in mysql_config and mysql_config[key] for key in required_keys_mysql):
        logger.error(f"MySQL configuration keys are missing or contain empty values: {mysql_config}")
        return None

    try:
        with SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(**ssh_config)

            with open_tunnel(
                (ssh_config['hostname'], int(ssh_config['port'])),
                ssh_username=ssh_config['username'],
                ssh_password=ssh_config['password'],
                remote_bind_address=(mysql_config['host'], int(mysql_config['port']))
            ) as tunnel:
                mysql_config['host'] = '127.0.0.1'
                mysql_config['port'] = tunnel.local_bind_port

                return mysql_query(mysql_config, query_sql)

    except Exception as e:
        logger.exception(f"An error occurred: {e}\n  ssh_config = {ssh_config}\n  mysql_config = {mysql_config}")
        return None
