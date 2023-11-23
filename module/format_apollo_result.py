"""
该模块提供了用于处理和格式化 Apollo 配置管理系统返回结果的功能。

主要包含 `format_apollo_result` 函数，用于将 Apollo 查询结果转换为更易于理解和使用的格式。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import datetime
import logging
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)


def format_apollo_result(app_id: str,
                         namespace_name: str,
                         rest: Tuple[str, str, datetime.datetime],
                         env_name: str) -> Optional[Dict[str, Dict[str, str]]]:
    """
    将 Apollo 查询结果格式化为更详细和易于理解的字典格式。

    此函数接收 Apollo 查询的基本信息和结果，然后转换为一个详细的字典，其中包括应用ID、命名空间、键值对和修改时间等信息。

    :param app_id: Apollo 应用的 ID。
    :type app_id: str
    :param namespace_name: Apollo 命名空间名称。
    :type namespace_name: str
    :param rest: 包含键、值和修改时间的元组。
    :type rest: Tuple[str, str, datetime.datetime]
    :param env_name: 环境名称。
    :type env_name: str
    :return: 格式化后的字典，如果处理过程中出现异常则返回 None。
    :rtype: Optional[Dict[str, Dict[str, str]]]

    :example:
    >>> format_apollo_result("app1", "namespace1", ("key1", "value1", datetime.datetime(2023, 10, 31, 0, 17, 43)), "dev")
    {'app1+namespace1+key1': {'app_id': 'app1', 'namespace_name': 'namespace1', 'key': 'key1', 'dev': 'value1', 'dev_modified_time': '2023-10-31 00:17:43'}}
    """
    try:
        key, env_value, modified_time = rest
        return {
            f"{app_id}+{namespace_name}+{key}": {
                'app_id': app_id,
                'namespace_name': namespace_name,
                'key': key,
                env_name: env_value,
                f'{env_name}_modified_time': modified_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    except Exception:
        logger.exception(f"Error occurred while formatting Apollo result: {env_name}, {app_id}, {namespace_name}")
        return None
