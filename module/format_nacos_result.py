"""
本模块提供了用于处理和格式化 Nacos 服务配置结果的功能。它主要处理 YAML 格式的配置内容，并将其转换为更易于使用的字典格式。

本模块适用于处理从 Nacos 获取的配置信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import datetime
import logging
from typing import Optional, Dict, Tuple

import yaml

from lib.dict_flatten import dict_flatten

logger = logging.getLogger(__name__)


def format_nacos_result(
        app_id: str,
        namespace_name: str,
        rest: Tuple[str, datetime.datetime],
        env_name: str
) -> Optional[Dict[str, Dict[str, str]]]:
    """
    将从 Nacos 获取的结果格式化为字典。

    此函数接收应用ID、命名空间名称、包含配置内容和修改时间的元组以及环境名称，解析配置内容并将其转换为字典格式。

    :param app_id: 应用的唯一标识符。
    :type app_id: str
    :param namespace_name: Nacos 配置的命名空间名称。
    :type namespace_name: str
    :param rest: 包含配置内容和最后修改时间的元组。
    :type rest: Tuple[str, datetime.datetime]
    :param env_name: 环境名称，例如 'prod', 'dev' 等。
    :type env_name: str
    :return: 格式化后的配置结果。如果解析或格式化失败，则返回 None。
    :rtype: Optional[Dict[str, Dict[str, str]]]

    :example:
    >>> format_nacos_result('track-web', 'namespace1', ('spring:\\n  application:\\n    name: track', datetime.datetime(2023, 10, 31, 1, 17, 43)), 'PRO')
    {'track-web+namespace1+spring.application.name': {'app_id': 'track-web', 'namespace_name': 'namespace1', 'key': 'spring.application.name', 'PRO': 'track', 'PRO_modified_time': '2023-10-31 01:17:43'}}
    """
    try:
        content, modified_time = rest

        # yaml解析原始内容，返回多重嵌套的字典
        yaml_content = yaml.safe_load(content)
        # yaml解析返回None或非字典，则打印警告，直接返回
        if not yaml_content or not isinstance(yaml_content, dict):
            logger.warning(f"Failed to parse yaml content:\n  {content}\nYAML content:\n  {yaml_content}\nfor app:\n  {env_name}, {app_id}, {namespace_name}")
            return None

        # 尝试将多重嵌套的字典，打平成properties格式。返回多个键值对的字典
        keys_and_values = dict_flatten(yaml_content)
        if not keys_and_values:
            logger.warning(f"Error flattening yaml content for:\n  {yaml_content}\nfor app:\n  {env_name}, {app_id}, {namespace_name}")
            return None

        return {
            f"{app_id}+{namespace_name}+{key}": {
                'app_id': app_id,
                'namespace_name': namespace_name,
                'key': key,
                env_name: value,
                f'{env_name}_modified_time': modified_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            for key, value in keys_and_values.items()
        }
    except Exception:
        logger.exception(f"Error occurred while formatting Nacos result: {env_name}, {app_id}, {namespace_name}")
        return None
