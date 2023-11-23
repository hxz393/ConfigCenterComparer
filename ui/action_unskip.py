"""
这是一个用于配置中心比较器的辅助模块，提供了取消跳过选定配置项的功能。

本模块主要包含 `ActionUnskip` 类，该类负责处理用户取消跳过特定配置项的操作。包括初始化取消跳过的按钮、绑定相关事件以及更新界面状态。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import CONFIG_SKIP_PATH, COL_INFO, COLOR_DEFAULT
from lib.get_resource_path import get_resource_path
from lib.read_file_to_list import read_file_to_list
from lib.write_list_to_file import write_list_to_file
from module.read_config import read_config

logger = logging.getLogger(__name__)


class ActionUnskip:
    """
    用于处理取消跳过配置项动作的类。

    此类封装了取消跳过配置项的界面逻辑，包括初始化取消跳过按钮、绑定相关事件、以及更新界面状态。

    :param main_window: 主窗口对象，用于访问和操作界面元素。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 `ActionUnskip` 类的实例。

        此方法负责设置界面元素，并绑定取消跳过按钮的动作。

        :param main_window: 主窗口对象，用于访问和操作界面元素。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.filter_bar = self.main_window.get_elements('filter_bar')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_unskip = QAction(QIcon(get_resource_path('media/icons8-ok-26.png')), self.lang['ui.action_unskip_1'], self.main_window)
        self.action_unskip.setShortcut('F5')
        self.action_unskip.setStatusTip(self.lang['ui.action_unskip_2'])
        self.action_unskip.triggered.connect(self.unskip_items)

    def unskip_items(self) -> None:
        """
        执行取消跳过选中配置项的动作。

        此方法读取当前选中的配置项，并将其从跳过列表中移除。同时更新状态栏的信息。

        :return: 无返回值。
        :rtype: None
        """
        try:
            skip_list = read_file_to_list(CONFIG_SKIP_PATH) or []
            config_main, config_connection = read_config()
            selected_keys = []

            # 重生成过滤列表
            for item in self.table.selectedItems():
                row = item.row()
                self.table.item(row, COL_INFO['skip']['col']).setData(Qt.UserRole, "no")
                self.table.item(row, COL_INFO['skip']['col']).setData(Qt.DisplayRole, self.lang['ui.action_start_11'])
                selected_keys.append(f"{self.table.item(row, COL_INFO['name']['col']).text()}+{self.table.item(row, COL_INFO['group']['col']).text()}+{self.table.item(row, COL_INFO['key']['col']).text()}")
                if config_main.get('color_set', 'ON') == 'ON':
                    self.table.apply_color(row, COLOR_DEFAULT)
                    self.table.apply_color_to_table([row], config_connection)

            skip_list = [f for f in skip_list if f not in selected_keys]
            self.filter_bar.filter_table()
            self.label_status.setText(self.lang['ui.action_unskip_3'])
            write_list_to_file(CONFIG_SKIP_PATH, set(skip_list))
        except Exception:
            logger.exception(f"An error occurred during unskip items")
            self.label_status.setText(self.lang['label_status_error'])
