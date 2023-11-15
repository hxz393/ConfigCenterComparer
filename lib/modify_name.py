"""
这个模块提供了名字修改的功能，包括根据前缀、后缀以及替换列表对名字进行修改。

主要包含 `modify_name` 函数，用于处理特定规则下的字符串替换和格式调整。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import List

logger = logging.getLogger(__name__)


def modify_name(name: str, search_items: List[str], replacement_items: List[str], prefixes: List[str], suffixes: List[str]) -> str:
    """
    修改给定名称，根据前缀、后缀和替换项进行调整。

    根据提供的前缀和后缀列表，首先从名称中移除这些前缀和后缀。然后，根据搜索项和替换项列表，将名称中的特定字符串替换为对应的替换字符串。

    :param name: 要修改的名字。
    :type name: str
    :param search_items: 需要搜索的项列表。
    :type search_items: List[str]
    :param replacement_items: 相应的替换项列表。
    :type replacement_items: List[str]
    :param prefixes: 需要检查的前缀列表。
    :type prefixes: List[str]
    :param suffixes: 需要检查的后缀列表。
    :type suffixes: List[str]
    :return: 修改后的名字。
    :rtype: str
    :raises Exception: 处理过程中发生任何异常。
    """
    try:
        name = next((name[len(prefix):] for prefix in prefixes if name.startswith(prefix)), name)
        name = next((name[:-len(suffix)] for suffix in suffixes if name.endswith(suffix)), name)
        return next((replacement_item for search_item, replacement_item in zip(search_items, replacement_items) if name == search_item), name)
    except Exception:
        logger.exception("Error occurred during name modification")
        return name
