"""
这是一个用于配置中心比较器的辅助模块，提供了跳过指定条目的功能。

此模块主要包含 `ActionSkip` 类，用于处理用户在配置比较过程中跳过特定项目的动作。它包括界面的初始化、事件绑定以及状态更新。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidgetItem

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import FILTER_PATH, COL_INFO
from lib.get_resource_path import get_resource_path
from lib.read_file_to_list import read_file_to_list
from lib.write_list_to_file import write_list_to_file

logger = logging.getLogger(__name__)


class ActionSkip:
    """
    用于处理跳过配置项动作的类。

    此类封装了跳过配置项的界面逻辑，包括初始化跳过按钮、绑定相关事件、以及更新界面状态。

    :param main_window: 主窗口对象，用于访问和操作界面元素。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 `ActionSkip` 类的实例。

        此方法负责设置界面元素，并绑定跳过按钮的动作。

        :param main_window: 主窗口对象，用于访问和操作界面元素。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.filter_bar = self.main_window.get_elements('filter_bar')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_skip = QAction(QIcon(get_resource_path('media/icons8-do-not-disturb-26.png')), self.lang['ui.action_skip_1'], self.main_window)
        self.action_skip.setShortcut('F4')
        self.action_skip.setStatusTip(self.lang['ui.action_skip_2'])
        self.action_skip.triggered.connect(self.skip_items)

    def skip_items(self) -> None:
        """
        执行跳过选中配置项的动作。

        此方法读取当前选中的配置项，并将其添加到跳过列表中。同时更新状态栏的信息。

        :return: 无返回值。
        :rtype: None
        """
        try:
            skip_list = read_file_to_list(FILTER_PATH) or []

            # 更新过滤器列表并写入文件
            skip_list.extend([self._get_index_key(item) for item in self.table.selectedItems()])
            write_list_to_file(FILTER_PATH, set(skip_list))

            self.filter_bar.filter_table()
            self.label_status.setText(self.lang['ui.action_skip_3'])
        except Exception:
            logger.exception(f"An error occurred during skip items")
            self.label_status.setText(self.lang['label_status_error'])

    def _get_index_key(self, item: QTableWidgetItem) -> str:
        """
        生成并返回表格项的索引键。

        该方法用于从表格项中提取必要信息，并生成一个用于标识该项的唯一索引键。

        :param item: 表格中的一个项目。
        :type item: QTableWidgetItem
        :return: 生成的索引键。
        :rtype: str
        """
        row = item.row()
        self.table.item(row, COL_INFO['skip']['col']).setData(Qt.UserRole, "1")
        self.table.item(row, COL_INFO['skip']['col']).setData(Qt.DisplayRole, self.lang['ui.action_start_12'])
        return f"{self.table.item(row, COL_INFO['name']['col']).text()}+{self.table.item(row, COL_INFO['group']['col']).text()}+{self.table.item(row, COL_INFO['key']['col']).text()}"