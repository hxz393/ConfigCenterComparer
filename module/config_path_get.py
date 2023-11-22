"""
这是一个用于管理和获取配置路径的模块。

此模块包含 `config_path_get` 函数，用于根据提供的配置中心字典获取相应的配置路径。支持的配置中心包括 Apollo 和 Nacos。

本模块的主要目的是提供一个统一的接口，通过配置中心的类型获取对应的配置文件路径。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, Dict

from config.settings import CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH

logger = logging.getLogger(__name__)


def config_path_get(config_main: Dict[str, str]) -> Optional[str]:
    """
    根据提供的配置字典获取相应的配置中心路径。

    此函数接收一个包含配置中心类型的字典，并根据其中的 'config_center' 键返回相应的配置路径。支持的配置中心类型包括 'Apollo' 和 'Nacos'。如果没有找到对应的类型或发生异常，则返回 None。

    :param config_main: 包含配置中心键值的字典。键 'config_center' 的值决定了将返回哪个配置中心的路径。
    :type config_main: Dict[str, str]
    :return: 如果找到对应的配置中心路径则返回该路径，否则返回 None。
    :rtype: Optional[str]

    :example:
    >>> config = {'config_center': 'Apollo'}
    >>> config_path_get(config)
    'config/config_apollo.json'
    """
    config_center_mapping = {
        'Apollo': CONFIG_APOLLO_PATH,
        'Nacos': CONFIG_NACOS_PATH
    }

    try:
        return config_center_mapping.get(config_main.get('config_center'), None)
    except Exception:
        logger.exception("Error occurred while getting configuration path")
        return None
