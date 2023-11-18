"""
此模块用于初始化和管理配置文件。

包含用于初始化配置文件的 `init_config` 函数，此函数检查配置文件的存在性，并根据需要创建默认配置文件。
这些配置文件包括主配置文件、跳过配置的列表文件、Apollo 和 Nacos 的连接配置文件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict, List, Union

from config.lang_dict_all import lang_dict_all
from config.settings import DEFAULT_CONFIG_CONNECTION, DEFAULT_CONFIG_MAIN, CONFIG_MAIN_PATH, CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH, CONFIG_SKIP_PATH
from lib.write_dict_to_json import write_dict_to_json
from lib.write_list_to_file import write_list_to_file
from module.read_config import read_config

logger = logging.getLogger(__name__)


def init_config() -> Dict[str, Union[str, List[str]]]:
    """
    初始化配置文件。

    检查各个配置文件是否存在，如果不存在，则根据默认值创建它们。这包括主配置文件、跳过配置的列表文件，以及Apollo和Nacos的连接配置文件。

    :return: 返回一个包含语言设置的字典。
    :rtype: Dict[str, Union[str, List[str]]]
    """
    try:
        config_paths = {
            CONFIG_MAIN_PATH: DEFAULT_CONFIG_MAIN,
            CONFIG_SKIP_PATH: [],
            CONFIG_APOLLO_PATH: DEFAULT_CONFIG_CONNECTION,
            CONFIG_NACOS_PATH: DEFAULT_CONFIG_CONNECTION,
        }
        for path, default in config_paths.items():
            if not os.path.isfile(path):
                if isinstance(default, list):
                    write_list_to_file(path, default)
                elif isinstance(default, dict):
                    write_dict_to_json(path, default)

        config_main, _ = read_config()
        return lang_dict_all[config_main.get('lang', 'English')]
    except Exception:
        logger.exception("Failed to initialize configuration")
        return lang_dict_all['English']
