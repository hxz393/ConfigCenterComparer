"""
这是一个用于测试数据库和SSH连接的Python模块。

本模块提供了 `test_connection` 函数，用于测试指定配置的MySQL数据库连接和SSH连接。
该函数接受一个包含数据库和SSH连接配置信息的字典参数，返回每个环境测试结果的列表。

主要用途是验证不同环境下的数据库和SSH连接状态。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, Dict, Any, List

from config.settings import SQL_TEST_MYSQL
from lib.mysql_query import mysql_query
from lib.mysql_query_with_ssh import mysql_query_with_ssh
from lib.ssh_test import ssh_test

logger = logging.getLogger(__name__)


def test_connection(config_connection: Dict[str, Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
    """
    测试数据库和SSH连接。

    通过提供的配置信息，此函数测试MySQL数据库连接和SSH连接。每个环境的测试结果将被收集并返回。

    :param config_connection: 包含每个环境的数据库和SSH连接配置信息的字典。
    :type config_connection: Dict[str, Dict[str, Any]]
    :return: 包含每个环境测试结果的列表。如果测试成功，返回测试结果；如果发生错误，返回 None。
    :rtype: Optional[List[Dict[str, Any]]]
    """
    try:
        test_result = []
        for env_name, config in config_connection.items():
            ssh_test_result = ssh_test(config['ssh']) if config.get('ssh_on') else None
            mysql_test_result = None

            if config.get('mysql_on'):
                mysql_test_result = mysql_query_with_ssh(config['ssh'], config['mysql'], SQL_TEST_MYSQL) if config.get('ssh_on') else mysql_query(config['mysql'], SQL_TEST_MYSQL)

            test_result.append({'env_name': env_name, 'ssh_test_result': ssh_test_result, 'mysql_test_result': mysql_test_result})

        return test_result
    except Exception:
        logger.exception(f"Error during connection test")
        return None
