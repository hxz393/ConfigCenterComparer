"""
这是一个用于获取配置路径的 Python 模块。

此模块包含一个主要函数 `get_config_path`，用于根据提供的配置字典获取相应的配置中心路径。支持的配置中心包括 Apollo 和 Nacos。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

from config.settings import CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH

# 初始化日志记录器
logger = logging.getLogger(__name__)


def config_path_get(config_dict: dict) -> Optional[str]:
    """
    根据提供的配置字典获取相应的配置中心路径。

    :param config_dict: 包含配置中心键值的字典。
    :type config_dict: dict
    :return: 如果找到对应的配置中心路径则返回该路径，否则返回 None。
    :rtype: Optional[str]
    """
    if not isinstance(config_dict, dict):
        logger.error("Provided configuration is not a dictionary.")
        return None

    config_center_mapping = {
        'Apollo': CONFIG_APOLLO_PATH,
        'Nacos': CONFIG_NACOS_PATH
    }

    try:
        config_type = config_dict.get('config_center')
        return config_center_mapping.get(config_type, None)
    except Exception as e:
        logger.exception(f"Invalid config center type: {e}")
        return None
