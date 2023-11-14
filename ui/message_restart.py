"""
提供用于重启应用程序的功能。

本文件包含一个函数 `message_restart`，用于显示消息框并在用户确认后重启应用程序。该功能主要用于应用程序的配置更改后的重启过程。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

# 初始化日志记录器
logger = logging.getLogger(__name__)


def message_restart(text: str) -> None:
    """
    显示消息框并在用户确认后重启应用程序。

    此函数会显示一个警告消息框，如果用户选择“Yes”，则会关闭当前应用程序并重新启动它。

    :param text: 要在消息框中显示的文本。
    :type text: str
    """
    try:
        reply = QMessageBox.question(None, 'Warning', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        QCoreApplication.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except Exception as e:
        logger.exception(f"Error during configuration change restart process: {e}")
