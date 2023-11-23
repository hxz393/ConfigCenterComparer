"""
这是一个Python文件，主要包含了一个用于 PyQt5 应用程序的类：`ActionSettingMain`。

`ActionSettingMain` 类定义了一个设置对话框的动作，用于在基于 PyQt5 的图形界面应用程序中创建和管理一个设置界面。此类接受一个 `ConfigCenterComparer` 实例作为主窗口对象，用于访问和操作界面元素。类中定义了用于初始化设置对话框动作和打开对话框的方法。

在类的 `__init__` 方法中，设置了设置对话框动作的图标、文本、快捷键等属性，并将其触发事件连接到打开对话框的方法。`open_dialog` 方法负责创建和执行对话框的显示操作。如果在打开对话框的过程中发生任何异常，类会捕获这些异常，并使用 `logging` 模块记录错误信息。

这个模块是构建基于 PyQt5 的图形界面应用程序的重要组成部分，主要用于提供应用程序的设置界面给用户。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from .dialog_settings_main import DialogSettingsMain

logger = logging.getLogger(__name__)


class ActionSettingMain:
    """
    定义一个设置对话框的动作类，用于在 PyQt5 应用程序中显示设置信息。

    :type main_window: ConfigCenterComparer
    :param main_window: 主窗口对象，用于访问和操作界面元素。
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 ActionSettingMain 类的实例。

        :param main_window: 主窗口对象，用于访问和操作界面元素。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_setting = QAction(QIcon(get_resource_path('media/icons8-setting-26.png')), self.lang['ui.action_setting_1'], self.main_window)
        self.action_setting.setStatusTip(self.lang['ui.action_setting_2'])
        self.action_setting.setShortcut('F11')
        self.action_setting.triggered.connect(self.open_dialog)

    def open_dialog(self) -> None:
        """
        打开设置对话框。

        :rtype: None
        :return: 无返回值。
        """
        try:
            dialog = DialogSettingsMain(self.main_window)
            dialog.exec_()
        except Exception:
            logger.exception(f"An error occurred while opening the settings dialog")
            self.label_status.setText(self.lang['label_status_error'])
