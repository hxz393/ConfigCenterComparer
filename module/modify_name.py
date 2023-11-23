"""
这个模块提供了名称修改功能，可以根据给定的前缀、后缀以及替换规则修改名称。

本模块的主要功能是 `modify_name` 函数，它可以根据用户提供的前缀、后缀列表和替换字典对名称进行修改。该功能对于处理需要去除特定前后缀或进行简单替换的字符串非常有用。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def modify_name(
        name: str,
        prefixes: List[str],
        suffixes: List[str],
        replacements: Dict[str, str]
) -> str:
    """
    根据指定的前缀、后缀列表和替换字典修改名称。

    此函数接收一个名称和三个列表：前缀列表、后缀列表和替换字典。它首先检查名称是否以列表中的任一个前缀或后缀开始或结束，如果是，则移除相应的前缀或后缀。之后，根据替换字典进行进一步替换。

    :param name: 要修改的原始名称。
    :type name: str
    :param prefixes: 用于检查和移除的前缀列表。
    :type prefixes: List[str]
    :param suffixes: 用于检查和移除的后缀列表。
    :type suffixes: List[str]
    :param replacements: 名称替换规则的字典。
    :type replacements: Dict[str, str]
    :return: 修改后的名称。
    :rtype: str

    :example:
    >>> modify_name("Mr. John Doe", ["Mr. ", "Mrs. "], [" Jr.", " Doe"], {"John": "Jonathan"})
    'Jonathan'
    """
    try:
        # 移除前缀，没有匹配则返回原始名
        name = next((name[len(prefix):] for prefix in prefixes if name.startswith(prefix)), name)

        # 移除后缀
        name = next((name[:-len(suffix)] for suffix in suffixes if name.endswith(suffix)), name)

        # 使用字典进行替换
        return replacements.get(name, name)
    except Exception:
        logger.exception(f"An error occurred when modifying name '{name}'")
        return name
