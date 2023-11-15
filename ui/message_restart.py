"""
这是一个用于处理应用程序重启的辅助模块。

本模块包含 `message_restart` 函数，该函数用于在用户确认后重启应用程序。在显示警告消息框时，用户可以选择是否重新启动应用程序。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


def message_restart(text: str) -> None:
    """
    显示消息框并在用户确认后重启应用程序。

    此函数会显示一个警告消息框，如果用户选择“Yes”，则会关闭当前应用程序并重新启动它。这通常用于应用配置更改后需要重新启动以应用更改的情况。

    :param text: 要在消息框中显示的文本，通常包含重启应用程序的提示信息。
    :type text: str
    :return: 无返回值。
    :rtype: None
    """
    try:
        reply = QMessageBox.question(None, 'Warning', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        QCoreApplication.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except Exception:
        logger.exception(f"Error during configuration change restart process")
