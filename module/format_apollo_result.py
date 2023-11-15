"""
这是一个用于处理和格式化 Apollo 配置管理服务结果的Python模块。

此模块提供了一个主要函数：`format_apollo_result`，用于将从 Apollo 服务获取的配置数据格式化为特定结构的字典。这主要用于解析配置管理服务的输出，将其转换为更易于处理和理解的格式。

本模块的主要目的是提供一个有效的方式来处理配置数据，确保在应用程序中易于访问和使用这些配置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


def format_apollo_result(app_id: str, namespace_name: str, rest: Tuple[str, str, Any], env_name: str) -> Optional[Dict[str, Dict[str, Any]]]:
    """
    格式化 Apollo 服务的结果。

    此函数解析从 Apollo 服务获取的配置数据，并将其转换为特定结构的字典格式。主要用于方便地存储和访问配置项。

    :param app_id: 应用的唯一标识符。
    :type app_id: str
    :param namespace_name: Apollo 中使用的命名空间名称。
    :type namespace_name: str
    :param rest: 包含配置键、环境值和最后修改时间的元组。
    :type rest: Tuple[str, str, Any]
    :param env_name: 对应的环境名称。
    :type env_name: str
    :return: 格式化后的字典，其中包含了配置项的详细信息。在解析异常时返回 None。
    :rtype: Optional[Dict[str, Dict[str, Any]]]
    """
    try:
        key, env_value, last_time = rest
        return {
            f"{app_id}+{namespace_name}+{key}": {
                'app_id': app_id,
                'namespace_name': namespace_name,
                'key': key,
                env_name: env_value,
                f'{env_name}_modified_time': str(last_time)
            }
        }
    except Exception:
        logger.exception("Error occurred while formatting Apollo result")
        return None
