"""
这是一个Python文件，用于初始化和获取应用程序的配置信息。

本文件包含一个主要函数：`config_init`。`config_init` 函数负责初始化配置并返回应用程序的主配置和连接配置。该函数尝试从预定义的配置文件路径读取配置信息。如果读取成功，返回包含主配置和连接配置的元组；如果失败，则返回默认配置。

在函数体中，首先尝试从 `CONFIG_MAIN_PATH` 读取主配置，然后从配置中获取连接配置的路径，并尝试读取连接配置。如果在这个过程中出现任何错误，函数会捕获异常，并使用 `logging` 模块记录错误信息，然后返回默认配置。

这个模块主要用于应用程序启动时的配置初始化，是应用程序运行的基础部分。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict, Tuple, Any, Optional

from .config_path_get import config_path_get
from lib.read_json_to_dict import read_json_to_dict
from config.settings import CONFIG_MAIN_PATH, DEFAULT_CONFIG_CONNECTION, DEFAULT_CONFIG_MAIN

# 初始化日志记录器
logger = logging.getLogger(__name__)


def config_init() -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """
    初始化并获取配置字典。

    尝试从配置文件路径读取配置，如果失败则返回默认配置。

    :rtype: Optional[Tuple[Dict[str, Any], Dict[str, Any]]]
    :return: 一个包含主配置和连接配置的元组，如果出现错误，则返回默认配置。
    """
    try:
        config_main = read_json_to_dict(os.path.normpath(CONFIG_MAIN_PATH)) or DEFAULT_CONFIG_MAIN
        config_connection = read_json_to_dict(os.path.normpath(config_path_get(config_main))) or DEFAULT_CONFIG_CONNECTION

        return config_main, config_connection
    except Exception as e:
        # 记录错误信息并返回默认配置
        logger.exception(f"An error occurred while initializing config: {e}")
        return DEFAULT_CONFIG_MAIN, DEFAULT_CONFIG_CONNECTION
