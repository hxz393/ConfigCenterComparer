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


def update_config_consistency_status(results: Dict[str, Dict[str, Any]], query_statuses: Dict[str, bool]) -> None:
    """
    更新配置的一致性状态。

    此函数接收两个字典参数：`results` 和 `query_statuses`。
    `results` 包含不同环境下配置文件的查询结果，`query_statuses` 包含各环境配置查询的状态（成功或失败）。
    函数遍历传入的配置结果字典，对每个配置项进行一致性判断，更新其一致性状态。

    完全一致（1）：所有配置项值相同；
    部分一致（2）：PRO和PRE环境配置项值相同，但不是全部；
    未知状态（3）：存在某个环境独有配置项值；
    不一致（0）：所有配置项值都不相同。

    :param results: 包含各环境下配置文件查询结果的字典。
    :type results: Dict[str, Dict[str, Any]]
    :param query_statuses: 包含各环境配置查询状态的字典。
    :type query_statuses: Dict[str, bool]
    """
    try:
        # 只对比查询成功的环境
        config_keys = [key for key, value in query_statuses.items() if value]
        for key, config in results.items():
            # 提取配置值，排除None
            values = [config[k] for k in config_keys if config.get(k) is not None]

            if len(values) <= 1:
                consistency_status = '3'
            elif all(val == values[0] for val in values) and len(values) == len(config_keys):
                consistency_status = '1'
            elif config.get('PRO_CONFIG') == config.get('PRE_CONFIG') and config.get('PRO_CONFIG') is not None:
                consistency_status = '2'
            else:
                consistency_status = '0'

            results[key]['consistency_status'] = consistency_status
    except Exception:
        logger.exception("Unexpected error occurred in update_config_consistency_status.")

