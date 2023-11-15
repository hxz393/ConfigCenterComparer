"""
这个Python文件包含一个用于将嵌套字典扁平化的功能。

`dict_flatten` 函数是这个文件的核心。它的主要目的是接受一个嵌套字典并将其转换为一个扁平化的字典，其中每个嵌套级别通过指定的分隔符连接。这对于配置处理非常有用，尤其是在需要将复杂的配置结构简化为一级键值对的场景中。

例如，它可以将形如 {'spring': {'application': {'name': 'ere-web'}}, 'server': {'port': 8080}} 的嵌套字典转换为 {'spring.application.name': 'ere-web', 'server.port': 8080} 的扁平字典。这种转换在处理例如从 YAML 或 JSON 文件读取的配置时特别有用。

如果在扁平化过程中遇到任何问题，函数将记录错误并返回 `None`。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def dict_flatten(content: Dict[Any, Any], parent_key: str = '', sep: str = '.') -> Optional[Dict[str, Any]]:
    """
    将嵌套的字典扁平化。通常用于配置中心格式互转。例如将 yaml 格式内容，用 yaml.safe_load 转为字典后，再消除嵌套。

    :type content: Dict[Any, Any]
    :param content: 要被扁平化的嵌套字典。

    :type parent_key: str
    :param parent_key: 上级键名，用于构建新键名。

    :type sep: str
    :param sep: 分隔符，用于连接键名。

    :rtype: Optional[Dict[str, Any]]
    :return: 扁平化后的字典，或在发生错误时返回 None。
    """
    try:
        items = {}
        for key, value in content.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.update(dict_flatten(value, new_key, sep=sep))
            else:
                items[new_key] = value
        return items
    except Exception:
        logger.exception(f"An error occurred while flattening the dictionary.")
        return None
