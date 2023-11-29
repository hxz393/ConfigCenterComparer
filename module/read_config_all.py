"""
这个模块提供了配置文件读取功能，主要用于从指定路径读取 JSON 格式的配置信息。

本模块主要包含 `read_config_all` 函数，用于读取主配置文件、Apollo 配置文件和 Nacos 配置文件。
读取的配置信息将用于应用程序的不同设置和操作。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict, Tuple, Optional, Union

from config.settings import CONFIG_MAIN_PATH, CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH, DEFAULT_CONFIG_CONNECTION, DEFAULT_CONFIG_MAIN
from lib.read_json_to_dict import read_json_to_dict

logger = logging.getLogger(__name__)


def read_config_all() -> Optional[Tuple[Dict[str, str], Dict[str, Dict[str, Union[Dict[str, str], bool]]], Dict[str, Dict[str, Union[Dict[str, str], bool]]]]]:
    """
    读取主配置文件、Apollo 配置文件和 Nacos 配置文件。

    此函数尝试从预定义路径读取 JSON 格式的配置文件，并将其转换为字典格式。如果读取失败，将返回默认配置。

    :param: 无
    :return: 包含三个配置字典的元组。第一个是主配置，第二个是 Apollo 配置，第三个是 Nacos 配置。
    :rtype: Optional[Tuple[Dict[str, str], Dict[str, Dict[str, Union[Dict[str, str], bool]]], Dict[str, Dict[str, Union[Dict[str, str], bool]]]]]

    :example:
    >>> os.chdir(os.path.dirname(os.getcwd()))
    >>> read_config_all()
    ({'key1': 'value1', 'key2': 'value2'}, {'apollo_key1': {'sub_key1': 'sub_value1', 'sub_key2': True}}, {'nacos_key1': {'sub_key1': 'sub_value1', 'sub_key2': False}})
    """
    try:
        config_main = read_json_to_dict(CONFIG_MAIN_PATH) or DEFAULT_CONFIG_MAIN
        config_apollo = read_json_to_dict(CONFIG_APOLLO_PATH) or DEFAULT_CONFIG_CONNECTION
        config_nacos = read_json_to_dict(CONFIG_NACOS_PATH) or DEFAULT_CONFIG_CONNECTION

        return config_main, config_apollo, config_nacos
    except Exception:
        # 记录错误信息并返回默认配置
        logger.exception("An error occurred while reading config")
        return DEFAULT_CONFIG_MAIN, DEFAULT_CONFIG_CONNECTION, DEFAULT_CONFIG_CONNECTION
