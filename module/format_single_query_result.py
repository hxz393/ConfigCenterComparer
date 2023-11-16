"""
这是一个用于处理和格式化配置中心查询结果的Python模块。

此模块提供了主要函数：`format_single_query_result`，用于根据不同的配置中心（如Apollo和Nacos）将查询结果格式化为特定结构的字典。这主要用于解析配置管理服务的输出，将其转换为更易于处理和理解的格式。

本模块的主要目的是提供一个有效的方式来处理来自不同配置中心的数据，并将其转换为统一格式的配置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any, Optional, Tuple

from .format_apollo_result import format_apollo_result
from .format_nacos_result import format_nacos_result
from .modify_name import modify_name

logger = logging.getLogger(__name__)


def format_single_query_result(single_query_result: Tuple[str, Any], env_name: str, name_config: Dict[str, Any]) -> Optional[Dict[str, Dict[str, Any]]]:
    """
    根据配置中心类型格式化单个查询结果。

    此函数接受单个查询结果，根据配置中心类型（如Apollo或Nacos）及环境名称来格式化结果。

    :param single_query_result: 单个查询结果，包括应用名、命名空间和其它数据。
    :type single_query_result: Tuple[str, str, Any]
    :param env_name: 环境名称。
    :type env_name: str
    :param name_config: 包含配置中心类型和其它配置的字典。
    :type name_config: Dict[str, Any]
    :return: 格式化后的字典，如果出现异常则返回 None。
    :rtype: Optional[Dict[str, Dict[str, Any]]]
    """
    try:
        app, namespace_name, *rest = single_query_result
        app_id = modify_name(app, name_config)

        if name_config['config_center'] == 'Apollo':
            return format_apollo_result(app_id, namespace_name, rest, env_name)
        else:
            return format_nacos_result(app_id, namespace_name, rest, env_name)
    except Exception:
        logger.exception(f"Error formatting query result: {single_query_result}")
        return None
