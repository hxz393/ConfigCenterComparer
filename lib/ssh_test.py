"""
这是一个Python文件，其中包含一个函数：`ssh_test`。

函数 `ssh_test` 用于测试SSH连接的有效性。它接收一个字典参数 `ssh_config`，包含了SSH连接所需的配置信息，例如主机名、端口、用户名和密码。函数首先检查配置信息是否完整且无空值。之后，创建一个SSH客户端，并使用配置信息尝试建立连接。连接成功返回0；如果配置信息有误，则返回-1；认证失败返回1；SSH连接异常返回2；其他任何异常则返回None。

本模块主要用于验证SSH配置信息的有效性，并尝试建立SSH连接。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

import paramiko

logger = logging.getLogger(__name__)


def ssh_test(ssh_config: dict) -> bool:
    """
    测试 SSH 连接是否成功。

    :param ssh_config: 包含 SSH 连接所需配置的字典。最基本的例如：{'hostname': '127.0.0.1', 'port': '22', 'username': 'root', 'password': 'abc123'}
    :type ssh_config: dict
    :rtype: bool
    :return: 连接成功返回 True，失败返回 False。
    """
    if not all(ssh_config.values()):
        logger.error("SSH configuration is incomplete or contains empty values")
        return False

    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(**ssh_config)
            return True
    except Exception:
        logger.exception("An unexpected error occurred。")
        return False
