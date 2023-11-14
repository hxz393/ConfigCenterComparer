"""
这是一个Python文件，主要包含了一个用于 PyQt5 应用程序的类：`ActionBlock`。

`ActionBlock` 类定义了一个加黑名单的动作，用于在基于 PyQt5 的图形界面应用程序中将选定的条目加入到黑名单。此类接受一个 `ConfigCenterComparer` 实例作为主窗口对象，用于访问和操作界面元素。类中定义了用于初始化加黑名单动作和执行加黑名单操作的方法。

在类的 `__init__` 方法中，设置了加黑名单动作的图标、文本、快捷键等属性，并将其触发事件连接到执行加黑名单操作的方法。`block_items` 方法负责执行加入黑名单的操作，包括更新表格显示、修改过滤列表和更新状态栏信息。如果在执行过程中发生任何异常，类会捕获这些异常，并使用 `logging` 模块记录错误信息。

这个模块是构建基于 PyQt5 的图形界面应用程序的重要组成部分，主要用于提供应用程序的动态黑名单功能给用户。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidgetItem

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from lib.read_file_to_list import read_file_to_list
from lib.write_list_to_file import write_list_to_file
from module.settings import FILTER_PATH

# 初始化日志记录器
logger = logging.getLogger(__name__)


class ActionBlock:
    """
    定义一个加黑名单动作的类，用于在 PyQt5 应用程序中加入选定的条目到黑名单。

    :type main_window: ConfigCenterComparer
    :param main_window: 主窗口对象，用于访问和操作界面元素。
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 ActionBlock 类的实例。

        :param main_window: 主窗口对象，用于访问和操作界面元素。
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.filter_bar = self.main_window.get_elements('filter_bar')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_block = QAction(QIcon(get_resource_path('media/icons8-do-not-disturb-26.png')), self.lang['ui.action_block_1'], self.main_window)
        self.action_block.setShortcut('F4')
        self.action_block.setStatusTip(self.lang['ui.action_block_2'])
        self.action_block.triggered.connect(self.block_items)

    def block_items(self) -> None:
        """
        执行加入黑名单的操作。

        :rtype: None
        :return: 无返回值。
        """
        try:
            filter_list = read_file_to_list(FILTER_PATH) or []

            # 更新过滤器列表并写入文件
            filter_list.extend([self._get_index_key(item) for item in self.table.selectedItems() if isinstance(item, QTableWidgetItem)])
            write_list_to_file(FILTER_PATH, set(filter_list))
            self.filter_bar.filter_table()
            self.label_status.setText(self.lang['ui.action_block_3'])

        except Exception as e:
            logger.exception(f"An error occurred during block_items execution: {e}")
            self.label_status.setText(self.lang['label_status_error'])

    def _get_index_key(self, item: QTableWidgetItem) -> str:
        """
        获取表格项的索引键。

        :param item: 表格项。
        :rtype: str
        :return: 索引键。
        """
        row = item.row()
        self.table.item(row, 8).setText("Yes")
        return f"{self.table.item(row, 0).text()}+{self.table.item(row, 1).text()}+{self.table.item(row, 2).text()}"
