"""
这是一个用于显示不同类型消息框的辅助模块。

本模块包含 `message_show` 函数，负责根据不同的消息类型显示相应的消息框。支持的消息类型包括 'Critical'、'Warning' 和 'Information'。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from lib.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


def message_show(message_type: str,
                 text: str) -> None:
    """
    显示指定类型的消息框。

    根据提供的消息类型和文本内容，显示相应的消息框。支持的消息类型包括 'Critical'、'Warning' 和 'Information'。

    :param message_type: 消息类型，支持 'Critical'、'Warning' 和 'Information'。
    :type message_type: str
    :param text: 消息框中显示的文本内容。
    :type text: str
    :return: 无返回值。
    :rtype: None
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
            logger.warning("Invalid message type provided.")

        msg_box.exec_()
    except Exception:
        logger.exception("An error occurred while displaying the message box")
