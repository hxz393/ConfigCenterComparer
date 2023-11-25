"""
本文件提供了对不同环境的数据库和SSH连接进行测试的功能。

通过定义的函数，我们可以测试指定配置的MySQL数据库和SSH连接的可用性。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, Dict, List, Union

from config.settings import SQL_TEST_MYSQL
from lib.mysql_query import mysql_query
from lib.mysql_query_with_ssh import mysql_query_with_ssh
from lib.ssh_test import ssh_test

logger = logging.getLogger(__name__)


def test_connection(config_connection: Dict[str, Dict[str, Union[Dict[str, str], bool]]]) -> Optional[List[Dict[str, Union[str, bool]]]]:
    """
    测试给定配置的数据库和SSH连接的可用性。

    此函数接收一个包含环境名称和其对应配置的字典。它会迭代这个字典，根据每个环境的配置进行MySQL数据库和SSH连接的测试。
    函数返回一个列表，包含每个环境的测试结果。

    :param config_connection: 包含环境配置的字典。键是环境名称，值是包含数据库和SSH配置的字典。
    :type config_connection: Dict[str, Dict[str, Union[Dict[str, str], bool]]]
    :return: 包含每个环境测试结果的列表。每个元素是一个字典，包含环境名称、SSH测试结果和MySQL测试结果。
    :rtype: Optional[List[Dict[str, Union[str, bool]]]]

    :example:
    >>> cc = {
    ...     "dev": {
    ...         "ssh_on": False,
    ...         "ssh": {"hostname": "192.168.0.1", "port": "22", "username": "user", "password": "pass"},
    ...         "mysql_on": True,
    ...         "mysql": {'host': '192.168.2.204', "port": "3306", "user": "root", "password": "QeqAr:%R+s5:hYnr", "db": "ApolloConfigDB_dev"}
    ...     }
    ... }
    >>> test_connection(cc)
    [{'env_name': 'dev', 'SSH': None, 'MySQL': True}]
    """
    try:
        test_result = []
        for env_name, config in config_connection.items():
            if config.get('ssh_on'):
                ssh_test_result = ssh_test(config['ssh'])
            else:
                ssh_test_result = None

            if config.get('mysql_on'):
                if config.get('ssh_on'):
                    mysql_test_result = mysql_query_with_ssh(config['ssh'], config['mysql'], SQL_TEST_MYSQL)
                else:
                    mysql_test_result = mysql_query(config['mysql'], SQL_TEST_MYSQL)

                if mysql_test_result:
                    mysql_test_result = True
            else:
                mysql_test_result = None
            test_result.append({'env_name': env_name, 'SSH': ssh_test_result, 'MySQL': mysql_test_result})
            logger.debug(f'ENV: {env_name} test finished')
        return test_result
    except Exception:
        logger.exception(f"Error during connection test")
        return None
