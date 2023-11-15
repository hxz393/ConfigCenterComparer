"""
这是一个用于配置中心比较器的辅助模块，主要提供数据保存功能。

本模块包含`ActionSave`类，负责处理来自配置中心比较器的数据的保存操作。它允许用户将表格数据保存到CSV或JSON文件中。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from module.save_data_to_file import save_data_to_file
from .message_show import message_show

logger = logging.getLogger(__name__)


class ActionSave:
    """
    处理配置中心比较器中数据的保存操作的类。

    此类提供了用户界面操作，允许用户将表格数据保存为CSV或JSON文件。它还包括错误处理和状态更新。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化保存操作。

        :param main_window: 配置中心比较器的主窗口对象。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_save = QAction(QIcon(get_resource_path('media/icons8-save-26.png')), self.lang['ui.action_save_1'], self.main_window)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.setStatusTip(self.lang['ui.action_save_2'])
        self.action_save.triggered.connect(self.save_file)

    def save_file(self) -> None:
        """
        触发保存文件的操作。

        此方法弹出文件保存对话框，允许用户选择保存格式和位置，并执行保存操作。
        """
        try:
            table_data = self.extract_table_data()
            if table_data is None:
                message_show('Critical', self.lang['ui.action_save_8'])
                return None

            file_name, file_type = QFileDialog.getSaveFileName(self.main_window, self.lang['ui.action_save_3'], "", "CSV Files (*.csv);;JSON Files (*.json)", options=QFileDialog.Options())
            if not file_name or not file_type:
                return None

            save_result = save_data_to_file(file_name, file_type, table_data)
            if save_result:
                self.label_status.setText(self.lang['ui.action_save_5'])
            else:
                message_show('Critical', self.lang['ui.action_save_7'])
        except Exception:
            logger.exception(f"Error saving file")
            self.label_status.setText(self.lang['label_status_error'])

    def extract_table_data(self) -> Optional[Dict[int, Dict[str, str]]]:
        """
        从表格中提取数据。

        此方法遍历配置中心比较器的表格，提取不隐藏的行和列的数据。

        :return: 表格数据的字典，键为行号，值为该行的数据字典；如果提取失败，则返回None。
        :rtype: Optional[Dict[int, Dict[str, str]]]
        """
        try:
            table_data = {
                row: {
                    self.table.horizontalHeaderItem(col).text(): self.table.item(row, col).text()
                    for col in range(self.table.columnCount()) if not self.table.isColumnHidden(col)
                }
                for row in range(self.table.rowCount()) if not self.table.isRowHidden(row)
            }
            return table_data
        except Exception:
            logger.exception("Error extracting data from the table")
            self.label_status.setText(self.lang['label_status_error'])
            return None
