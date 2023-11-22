"""
本模块提供了根据配置获取语言字典的功能。

主要功能集中在 `get_lang_dict` 函数，它根据当前配置返回相应的语言字典。该功能对于多语言环境下的语言选择和应用非常有用。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict

from config.lang_dict_all import LANG_DICTS
from module.read_config import read_config

logger = logging.getLogger(__name__)


def get_lang_dict() -> Dict[str, str]:
    """
    根据当前配置获取相应的语言字典。

    本函数从配置文件中读取当前语言设置，并根据该设置返回对应的语言字典。如果读取配置时发生异常，将默认返回英文语言字典。

    :return: 语言字典，键为字符串标识，值为对应的翻译文本。
    :rtype: Dict[str, str]
    :example:
    >>> os.chdir(os.path.dirname(os.getcwd()))
    >>> get_lang_dict()
    """
    try:
        config_main, _ = read_config()
        return LANG_DICTS[config_main.get('lang', 'English')]
    except Exception:
        logger.exception("Failed to get language dictionary")
        return LANG_DICTS['English']
