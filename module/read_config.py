"""
本文件提供了配置读取功能，主要用于从配置文件中读取和解析配置信息。

本模块的核心是 `read_config` 函数，它从给定的配置文件路径中读取配置信息，如果读取失败则返回默认配置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict, Tuple, Optional, Union

from config.settings import CONFIG_MAIN_PATH, DEFAULT_CONFIG_CONNECTION, DEFAULT_CONFIG_MAIN
from lib.read_json_to_dict import read_json_to_dict
from module.config_path_get import config_path_get

logger = logging.getLogger(__name__)


def read_config() -> Optional[Tuple[Dict[str, str], Dict[str, Dict[str, Union[Dict[str, str], bool]]]]]:
    """
    初始化并获取配置字典。

    尝试从配置文件路径读取配置，如果失败则返回默认配置。此函数主要用于加载和处理应用程序的配置文件。

    :return: 一个包含主配置和连接配置的元组，如果出现错误，则返回默认配置。
    :rtype: Optional[Tuple[Dict[str, str], Dict[str, Dict[str, Union[Dict[str, str], bool]]]]]
    :example:
    >>> main_config, _ = read_config()
    >>> assert isinstance(main_config, dict)
    >>> os.chdir(os.path.dirname(os.getcwd()))
    >>> _, connection_config = read_config()
    >>> assert isinstance(connection_config, dict)
    """
    try:
        config_main = read_json_to_dict(CONFIG_MAIN_PATH) or DEFAULT_CONFIG_MAIN
        config_connection = read_json_to_dict(config_path_get(config_main)) or DEFAULT_CONFIG_CONNECTION

        return config_main, config_connection
    except Exception:
        # 记录错误信息并返回默认配置
        logger.exception(f"An error occurred while reading config")
        return DEFAULT_CONFIG_MAIN, DEFAULT_CONFIG_CONNECTION
