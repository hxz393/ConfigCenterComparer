"""
这是一个用于处理配置文件一致性检查的Python模块。

此模块提供了一个主要函数：`update_config_consistency_status`，用于更新和检查各环境下配置文件的一致性状态。该函数通过比较不同环境（如生产、预发布、开发和测试）下的配置文件，判断它们是否一致。

主要目的是为了确保各环境配置的一致性，便于在软件部署和运维过程中快速识别配置差异。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def update_config_consistency_status(results: Dict[str, Dict[str, Any]]) -> None:
    """
    更新配置的一致性状态。

    此函数遍历传入的配置结果字典，对每个配置项进行一致性判断。一致性状态分为完全一致、部分一致和不一致三种。
    完全一致（1）：所有配置项值相同；
    部分一致（2）：PRO和PRE环境配置项值相同，但不是全部；
    不一致（0）：所有配置项值都不相同。

    :param results: 包含多个环境配置的字典。
    :type results: Dict[str, Dict[str, Any]]
    """
    config_keys = ['PRO_CONFIG', 'PRE_CONFIG', 'DEV_CONFIG', 'TEST_CONFIG']

    try:
        for key, config in results.items():
            # 提取配置值，排除None
            values = [config[k] for k in config_keys if config.get(k) is not None]

            if len(values) <= 1:
                consistency_status = '0'
            elif all(val == values[0] for val in values):
                consistency_status = '1'
            elif config.get('PRO_CONFIG') == config.get('PRE_CONFIG'):
                consistency_status = '2'
            else:
                consistency_status = '0'

            results[key]['equal'] = consistency_status
    except Exception:
        logger.exception("Unexpected error occurred in update_config_consistency_status.")

