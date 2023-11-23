"""
这个模块提供了配置一致性状态的确定功能。它可以根据提供的配置值列表、配置字典和有效键列表来判断配置的一致性状态。

本模块的主要功能是 `determine_consistency_status` 函数，它能够根据配置值的比较结果返回相应的一致性状态。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def determine_consistency_status(
        values: List[str],
        config: Dict[str, str],
        valid_keys: List[str]
) -> str:
    """
    配置的一致性状态判断逻辑。

    此函数接收三个参数：配置值列表、配置字典和有效键列表。它将这些参数用于判断配置的一致性状态，并返回状态描述。状态描述可以是 'unknown', 'fully', 'partially', 或 'inconsistent'。

    :param values: 配置值列表，已排除空值。
    :type values: List[str]
    :param config: 包含配置项的字典。
    :type config: Dict[str, str]
    :param valid_keys: 有效的环境列表，用于确定哪些环境参与对比。也就是mysql_on为开启时才在列表中。
    :type valid_keys: List[str]
    :return: 配置的一致性状态描述。
    :rtype: str

    :example:
    >>> determine_consistency_status(["val1", "val1", "val1"], {"PRO_CONFIG": "val1", "PRE_CONFIG": "val1", "TEST_CONFIG": "val1"}, ["PRO_CONFIG", "PRE_CONFIG", "TEST_CONFIG"])
    'fully'
    >>> determine_consistency_status(["val1", "val1", "val2"], {"PRO_CONFIG": "val1", "PRE_CONFIG": "val1", "TEST_CONFIG": "val2"}, ["PRO_CONFIG", "PRE_CONFIG", "TEST_CONFIG"])
    'partially'
    >>> determine_consistency_status(["val1"], {"PRO_CONFIG": "val1", "PRE_CONFIG": None}, ["PRO_CONFIG", "PRE_CONFIG"])
    'unknown'
    >>> determine_consistency_status(["val1", "val1"], {"PRO_CONFIG": "val1", "PRE_CONFIG": None, "TEST_CONFIG": "val1"}, ["PRO_CONFIG", "PRE_CONFIG", "TEST_CONFIG"])
    'inconsistent'
    """
    try:
        # 有效配置值小于等于1
        if len(values) <= 1:
            return 'unknown'

        # 在开启对比环境中，所有值相等。没有开启的环境不参与对比（比如valid_keys有PRO，但是PRO配置值为None，则values中被排除，两个表长度不等）。
        first_value = values[0]
        if all(val == first_value for val in values) and len(values) == len(valid_keys):
            return 'fully'

        # 正式环境有值，且正式环境值等于预览环境值。
        pro_config = config.get('PRO_CONFIG')
        pre_config = config.get('PRE_CONFIG')
        if pro_config == pre_config and pro_config is not None:
            return 'partially'

        # 其他所有情况。
        return 'inconsistent'
    except Exception:
        logger.exception(f"Error occurred in determining consistency status. Error config: {config}")
        return 'unknown'
