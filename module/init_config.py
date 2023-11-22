"""
这个模块提供了配置初始化功能，主要用于检查和初始化各种配置文件。

模块的核心是 `init_config` 函数，它负责检查一系列配置文件的存在性，若不存在则创建默认配置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
import shutil

from config.settings import DEFAULT_CONFIG_CONNECTION, DEFAULT_CONFIG_MAIN, CONFIG_MAIN_PATH, CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH, CONFIG_SKIP_PATH
from lib.write_dict_to_json import write_dict_to_json
from lib.write_list_to_file import write_list_to_file

logger = logging.getLogger(__name__)


def init_config() -> None:
    """
    检查并初始化配置文件。

    此函数遍历预定义的配置文件路径列表，检查每个配置文件是否存在。若不存在，根据配置类型（列表或字典）使用适当的方法创建默认配置。

    :return: 无返回值。
    :rtype: None

    :example:
    >>> init_config()  # 创建默认配置文件，检查生成的文件内容
    >>> shutil.rmtree('config')
    """
    try:
        config_paths_and_default_configs = {
            CONFIG_MAIN_PATH: DEFAULT_CONFIG_MAIN,
            CONFIG_SKIP_PATH: [],
            CONFIG_APOLLO_PATH: DEFAULT_CONFIG_CONNECTION,
            CONFIG_NACOS_PATH: DEFAULT_CONFIG_CONNECTION,
        }
        # 逐个文件路径检查，如果文件不存在，则创建默认配置。
        for path, config in config_paths_and_default_configs.items():
            if not os.path.isfile(path):
                # 根据配置格式不同，调用不同写入函数。
                if isinstance(config, list):
                    write_list_to_file(path, config)
                elif isinstance(config, dict):
                    write_dict_to_json(path, config)
    except Exception:
        logger.exception("Failed to initialize configuration")
