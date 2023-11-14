"""
这个 Python 文件包含了一个用于显示消息框的函数：`message_show`。

`message_show` 函数的主要目的是根据提供的消息类型和文本，显示一个消息框。它接受两个参数：`message_type` 和 `text`。 `message_type` 参数决定了消息框的类型，可以是 'Warning' 或 'Information'。`text` 参数是消息框中显示的文本内容。

在函数体中，首先创建一个 `QMessageBox` 对象，并根据 `message_type` 设置不同的图标和窗口图标。然后，函数显示消息框。如果过程中遇到任何异常，函数会捕获异常并使用 `logging` 模块记录错误信息，然后返回 `None`。

这个模块主要用于在图形用户界面中显示警告或信息类的消息框，是用户交互的一个重要组成部分。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from lib.get_resource_path import get_resource_path

# 初始化日志记录器
logger = logging.getLogger(__name__)


def message_show(message_type: str, text: str) -> None:
    """
    显示消息框。

    :param message_type: 消息类型，支持 'Warning' 或 'Information'。
    :type message_type: str
    :param text: 消息框中显示的文本。
    :type text: str
    :return: 无返回值
    """
    try:
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowTitle(message_type)

        if message_type == 'Critical':
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowIcon(QIcon(get_resource_path('media/icons8-error-26')))
        elif message_type == 'Warning':
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowIcon(QIcon(get_resource_path('media/icons8-do-not-disturb-26')))
        elif message_type == 'Information':
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowIcon(QIcon(get_resource_path('media/icons8-about-26')))
        else:
            raise ValueError("Invalid message type provided.")

        msg_box.exec_()
    except Exception:
        logger.exception(f"An error occurred while displaying the message box")
