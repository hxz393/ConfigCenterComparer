"""
这是一个用于处理名称修改和配置的Python模块。

此模块包含主要的 `modify_name` 函数，负责根据配置处理和修改指定的名称，包括去除前缀和后缀，以及替换名称。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any

# 初始化日志记录器
logger = logging.getLogger(__name__)


def modify_name(name: str, name_config: Dict[str, Any]) -> str:
    """
    修改名称，根据配置文件进行前缀、后缀修剪和名称替换。

    该函数接受一个名称和一个配置字典。首先，它会检查并移除名称的前缀和后缀，然后根据配置替换整个名称。如果在处理过程中发生异常，将记录异常信息并返回原始名称。

    :param name: 要修改的名字。
    :type name: str
    :param name_config: 包含名称修改配置的字典，如前缀、后缀和替换规则。
    :type name_config: Dict[str, Any]
    :return: 修改后的名字。如果处理过程中发生异常，则返回原始名称。
    :rtype: str
    """
    try:
        search_items = name_config['fix_name_before'].split()
        replacement_items = name_config['fix_name_after'].split()
        prefixes = name_config['fix_name_left'].split()
        suffixes = name_config['fix_name_right'].split()

        # 移除前缀
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break

        # 移除后缀
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break

        # 替换名称
        for search_item, replacement_item in zip(search_items, replacement_items):
            if name == search_item:
                return replacement_item

        return name
    except Exception:
        logger.exception("An error occurred in modify_name")
        return name
