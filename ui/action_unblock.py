"""
这是一个Python文件，主要包含了一个用于 PyQt5 应用程序的类：`ActionUnblock`。

`ActionUnblock` 类定义了一个解锁动作，用于在基于 PyQt5 的图形界面应用程序中解锁选定的条目。此类接受一个 `ConfigCenterComparer` 实例作为主窗口对象，用于访问和操作界面元素。类中定义了用于初始化解锁动作和执行解锁操作的方法。

在类的 `__init__` 方法中，设置了解锁动作的图标、文本、快捷键等属性，并将其触发事件连接到执行解锁操作的方法。`unblock_items` 方法负责执行解锁选定条目的操作，包括更新表格显示、修改过滤列表和更新状态栏信息。如果在执行过程中发生任何异常，类会捕获这些异常，并使用 `logging` 模块记录错误信息。

这个模块是构建基于 PyQt5 的图形界面应用程序的重要组成部分，主要用于提供应用程序的动态解锁功能给用户。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from lib.read_file_to_list import read_file_to_list
from lib.write_list_to_file import write_list_to_file
from config.settings import FILTER_PATH

# 初始化日志记录器
logger = logging.getLogger(__name__)


class ActionUnblock:
    """
    定义一个解锁动作的类，用于在 PyQt5 应用程序中解锁选定的条目。

    :type main_window: ConfigCenterComparer
    :param main_window: 主窗口对象，用于访问和操作界面元素。
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 ActionUnblock 类的实例。

        :param main_window: 主窗口对象，用于访问和操作界面元素。
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.filter_bar = self.main_window.get_elements('filter_bar')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_unblock = QAction(QIcon(get_resource_path('media/icons8-ok-26.png')), self.lang['ui.action_unblock_1'], self.main_window)
        self.action_unblock.setShortcut('F5')
        self.action_unblock.setStatusTip(self.lang['ui.action_unblock_2'])
        self.action_unblock.triggered.connect(self.unblock_items)

    def unblock_items(self) -> None:
        """
        执行解锁选定条目的操作。

        :rtype: None
        :return: 无返回值。
        """
        try:
            filter_list = read_file_to_list(FILTER_PATH) or []

            for item in self.table.selectedItems():
                row = item.row()
                self.table.item(row, 8).setText("No")
                index_key = f"{self.table.item(row, 0).text()}+{self.table.item(row, 1).text()}+{self.table.item(row, 2).text()}"
                # 重生成过滤列表
                filter_list = [f for f in filter_list if f != index_key]

            write_list_to_file(FILTER_PATH, set(filter_list))
            self.filter_bar.filter_table()
            self.label_status.setText(self.lang['ui.action_unblock_3'])

        except Exception:
            logger.exception(f"An error occurred during unblock_items execution")
            self.label_status.setText(self.lang['label_status_error'])
