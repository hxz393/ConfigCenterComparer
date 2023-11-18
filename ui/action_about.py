"""
这是一个Python文件，主要包含了一个用于 PyQt5 应用程序的类：`ActionAbout`。

`ActionAbout` 类用于在 PyQt5 基于的图形界面应用程序中创建和管理一个“关于”对话框的动作。这个类接受一个 `ConfigCenterComparer` 实例作为主窗口对象，以便访问和操作界面元素。类中定义了用于初始化动作和打开对话框的方法。

在类的 `__init__` 方法中，设置了关于动作的图标、文本、快捷键等属性，并将其触发事件连接到打开对话框的方法。`open_dialog` 方法负责创建和执行对话框的显示操作。如果在打开对话框的过程中发生任何异常，类会捕获这些异常，并使用 `logging` 模块记录错误信息。

这个模块是构建基于 PyQt5 的图形界面应用程序的重要组成部分，主要用于提供应用程序的基本信息给用户。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from .dialog_about import DialogAbout

logger = logging.getLogger(__name__)


class ActionAbout:
    """
    定义一个关于对话框的动作类，用于在 PyQt5 应用程序中显示关于信息。

    :type main_window: ConfigCenterComparer
    :param main_window: 主窗口对象，用于访问和操作界面元素。
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 ActionAbout 类的实例。

        :param main_window: 主窗口对象，用于访问和操作界面元素。
        """
        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_about = QAction(QIcon(get_resource_path('media/icons8-about-26.png')), self.lang['ui.action_about_1'], self.main_window)
        self.action_about.setStatusTip(self.lang['ui.action_about_2'])
        self.action_about.setShortcut('F1')
        self.action_about.triggered.connect(self.open_dialog)

    def open_dialog(self) -> None:
        """
        打开关于对话框。

        :rtype: None
        :return: 无返回值。
        """
        try:
            dialog = DialogAbout(self.main_window)
            dialog.exec_()
        except Exception:
            logger.exception(f"An error occurred while opening the about dialog")
            self.label_status.setText(self.lang['label_status_error'])
