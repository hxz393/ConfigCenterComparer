"""
本模块提供用户界面中的动作处理功能，尤其是忽略选中项的功能。

此模块包含 `ActionSkip` 类，用于实现忽略选中项目的动作。该类负责处理用户界面的忽略动作，并与配置管理器和语言管理器交互以更新用户界面。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import List

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidget

from config.settings import CONFIG_SKIP_PATH, COL_INFO
from lib.get_resource_path import get_resource_path
from lib.write_list_to_file import write_list_to_file
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionSkip(QObject):
    """
    处理用户界面中忽略操作的类。

    :param lang_manager: 语言管理器，用于处理界面语言设置。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器，用于管理应用配置。
    :type config_manager: ConfigManager
    :param table: 主表格界面对象。
    :type table: QTableWidget
    """
    status_updated = pyqtSignal(str)
    filter_updated = pyqtSignal()
    color_updated = pyqtSignal(list, dict)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 table: QTableWidget):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.table = table
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_skip = QAction(QIcon(get_resource_path('media/icons8-do-not-disturb-26.png')), 'Skip')
        self.action_skip.setShortcut('F4')
        self.action_skip.triggered.connect(self.skip_items)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_skip.setText(self.lang['ui.action_skip_1'])
        self.action_skip.setStatusTip(self.lang['ui.action_skip_2'])

    def skip_items(self) -> None:
        """
        执行忽略选中项目的操作。

        此方法负责更新忽略列表，并将其写入配置文件。同时更新配置管理器中的配置，并重新应用过滤器。

        :rtype: None
        :return: 无返回值。
        """
        try:
            updated_skip_list = self.update_skip_list_and_apply_color()
            # 写入到配置文件
            write_list_to_file(CONFIG_SKIP_PATH, updated_skip_list)
            # 更新配置管理器中的配置
            self.config_manager.update_skip_list(updated_skip_list)
            # 重新应用过略器
            self.filter_updated.emit()
            # 发送到状态栏
            self.status_updated.emit(self.lang['ui.action_skip_3'])
            logger.info(f"Items skipped. Skip list length: {len(updated_skip_list)}")
        except Exception:
            logger.exception("Error occurred while skipping items")
            self.status_updated.emit(self.lang['label_status_error'])

    def update_skip_list_and_apply_color(self) -> List[str]:
        """
        更新忽略列表并应用颜色。

        此方法遍历选中的项目，将它们添加到忽略列表，并应用配置的颜色设置。

        :rtype: List[str]
        :return: 更新后的忽略列表。
        """
        # 获取配置
        config_main = self.config_manager.get_config_main()
        config_connection = self.config_manager.get_config_connection()
        skip_list = self.config_manager.get_skip_list()

        for item in self.table.selectedItems():
            row = item.row()
            self.update_table_item(row)
            skip_list.append(f"{self.table.item(row, COL_INFO['name']['col']).text()}+{self.table.item(row, COL_INFO['group']['col']).text()}+{self.table.item(row, COL_INFO['key']['col']).text()}")
            if config_main.get('color_set', 'ON') == 'ON':
                self.color_updated.emit([row], config_connection)

        return list(set(skip_list))

    def update_table_item(self, row: int) -> None:
        """
        更新表格中指定行的项目。

        此方法设置指定行的项目为“已忽略”。

        :param row: 要更新的行。
        :type row: int
        :rtype: None
        :return: 无返回值。
        """
        self.table.item(row, COL_INFO['skip']['col']).setData(Qt.UserRole, "yes")
        self.table.item(row, COL_INFO['skip']['col']).setData(Qt.DisplayRole, self.lang['ui.action_start_12'])
