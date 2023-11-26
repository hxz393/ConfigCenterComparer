"""
此模块提供了用于处理表格数据保存功能的类。

类 `ActionSave` 封装了与数据保存相关的所有操作，包括初始化界面、更新语言设置以及执行保存动作。
此类是与 PyQt5 相关的 GUI 操作的一部分，用于实现用户的数据保存需求。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict, Optional

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QTableWidget

from lib.get_resource_path import get_resource_path
from module.save_data_to_file import save_data_to_file
from ui.lang_manager import LangManager
from ui.message_show import message_show

logger = logging.getLogger(__name__)


class ActionSave(QObject):
    """
    实现表格数据的保存功能。

    此类用于在表格界面中提供保存操作，允许用户将表格数据保存到文件。

    :param lang_manager: 用于管理语言设置的对象。
    :type lang_manager: LangManager
    :param table: 表格对象，用于操作表格数据。
    :type table: QTableWidget
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 table: QTableWidget):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.table = table
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_save = QAction(QIcon(get_resource_path('media/icons8-save-26.png')), 'Save')
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.triggered.connect(self.save_file)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_save.setText(self.lang['ui.action_save_1'])
        self.action_save.setStatusTip(self.lang['ui.action_save_2'])

    def save_file(self) -> None:
        """
        触发保存文件的操作。

        此方法弹出文件保存对话框，允许用户选择保存格式和位置，并执行保存操作。

        :rtype: None
        :return: 无返回值。
        """
        try:
            table_data = self._extract_table_data()
            if table_data is None:
                message_show('Critical', self.lang['ui.action_save_8'])
                return None

            file_name, file_type = QFileDialog.getSaveFileName(None, self.lang['ui.action_save_3'], "", "CSV Files (*.csv);;JSON Files (*.json)", options=QFileDialog.Options())
            if not file_name or not file_type:
                return None

            save_result = save_data_to_file(file_name, file_type, table_data)
            if save_result:
                self.status_updated.emit(self.lang['ui.action_save_5'])
                logger.info(f"File saved to: '{file_name}', File size: {os.path.getsize(file_name):,} Bytes")
            else:
                message_show('Critical', self.lang['ui.action_save_7'])
        except Exception:
            logger.exception("Error saving file")
            self.status_updated.emit(self.lang['label_status_error'])

    def _extract_table_data(self) -> Optional[Dict[int, Dict[str, str]]]:
        """
        从表格中提取数据。

        此方法遍历配置中心比较器的表格，提取不隐藏的行和列的数据。

        :return: 表格数据的字典，键为行号，值为该行的数据字典；如果提取失败，则返回None。
        :rtype: Optional[Dict[int, Dict[str, str]]]
        """
        return {
            row: {
                self.table.horizontalHeaderItem(col).text(): self.table.item(row, col).text()
                for col in range(self.table.columnCount()) if not self.table.isColumnHidden(col)
            }
            for row in range(self.table.rowCount()) if not self.table.isRowHidden(row)
        }
