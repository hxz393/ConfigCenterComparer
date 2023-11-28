"""
本模块提供用户界面中的动作处理功能，尤其是取消忽略选中项的功能。

此模块包含 `ActionUnskip` 类，用于实现取消忽略选中项目的动作。该类负责处理用户界面的取消忽略动作，并与配置管理器和语言管理器交互以更新用户界面。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QAction, QTableWidget

from config.settings import COL_INFO, COLOR_DEFAULT
from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionUnskip(QObject):
    """
    处理用户界面中取消忽略操作的类。

    :param lang_manager: 语言管理器，用于处理界面语言设置。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器，用于管理应用配置。
    :type config_manager: ConfigManager
    :param table: 主表格界面对象。
    :type table: QTableWidget
    """
    status_updated = pyqtSignal(str)
    filter_updated = pyqtSignal(list)
    color_updated = pyqtSignal(list)

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
        self.action_unskip = QAction(QIcon(get_resource_path('media/icons8-ok-26.png')), 'UnSkip')
        self.action_unskip.setShortcut('F5')
        self.action_unskip.triggered.connect(self.unskip_items)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_unskip.setText(self.lang['ui.action_unskip_1'])
        self.action_unskip.setStatusTip(self.lang['ui.action_unskip_2'])

    def unskip_items(self) -> None:
        """
        执行取消忽略选中项目的操作。

        此方法负责更新忽略列表，并将其写入配置文件。同时更新配置管理器中的配置，并重新应用过滤器。

        :rtype: None
        :return: 无返回值。
        """
        try:
            updated_skip_list = self.update_skip_list()
            # 更新配置管理器中的配置
            self.config_manager.update_skip_list(updated_skip_list)
            # 重新应用过略器
            self.filter_updated.emit([item.row() for item in self.table.selectedItems()])
            # 发送到状态栏
            self.status_updated.emit(self.lang['ui.action_unskip_3'])
            logger.info(f"Items unskipped. Skip list length: {len(updated_skip_list)}")
        except Exception:
            logger.exception("Error occurred while unskipping items")
            self.status_updated.emit(self.lang['label_status_error'])

    def update_skip_list(self) -> list:
        """
        更新忽略列表并应用颜色。

        此方法遍历选中的项目，将它们从忽略列表去除。

        :rtype: List[str]
        :return: 更新后的忽略列表。
        """
        # 获取配置
        skip_list = self.config_manager.get_skip_list()
        selected_keys = []

        for item in self.table.selectedItems():
            row = item.row()
            self.update_table_item(row)
            selected_keys.append(f"{self.table.item(row, COL_INFO['name']['col']).text()}+{self.table.item(row, COL_INFO['group']['col']).text()}+{self.table.item(row, COL_INFO['key']['col']).text()}")

        return list(set([f for f in skip_list if f not in selected_keys]))

    def update_table_item(self, row: int) -> None:
        """
        更新表格中指定行的项目。

        此方法设置指定行的项目为“不忽略”。

        :param row: 要更新的行。
        :type row: int
        :rtype: None
        :return: 无返回值。
        """
        self.table.item(row, COL_INFO['skip']['col']).setData(Qt.UserRole, "no")
        self.table.item(row, COL_INFO['skip']['col']).setData(Qt.DisplayRole, self.lang['ui.action_start_11'])
