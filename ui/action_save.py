"""
这是一个用于处理配置中心比较器界面中的保存操作的模块。

此模块包含 `ActionSave` 类，该类负责管理保存操作，包括提取表格数据、显示保存对话框，以及将数据保存为 CSV 或 JSON 文件。

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
from lib.write_dict_to_csv import write_dict_to_csv
from lib.write_dict_to_json import write_dict_to_json
from .message_show import message_show

# 初始化日志记录器
logger = logging.getLogger(__name__)


class ActionSave:
    """
    处理配置中心比较器界面中的保存操作的类。

    此类封装了与保存操作相关的逻辑，包括初始化保存动作、绑定事件以及处理文件保存过程。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_save = QAction(QIcon(get_resource_path('media/icons8-save-26.png')), self.lang['ui.action_save_1'], self.main_window)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.setStatusTip(self.lang['ui.action_save_2'])
        self.action_save.triggered.connect(self.save_file)

    def extract_table_data(self) -> Optional[Dict[int, Dict[str, str]]]:
        """
        提取表格数据。

        此方法遍历表格中的每一行，构建一个包含所有可见行数据的字典。

        :rtype: Optional[Dict[int, Dict[str, str]]]
        :return: 包含表格数据的字典，如果出现错误则返回 None。
        """
        try:
            data = {}
            for row in range(self.table.rowCount()):
                if not self.table.isRowHidden(row):
                    data[row] = {self.table.horizontalHeaderItem(col).text(): self.table.item(row, col).text() for col in range(self.table.columnCount())}
            return data
        except Exception:
            logger.exception(f"Error extracting data from the table")
            self.label_status.setText(self.lang['label_status_error'])
            return None

    def save_file(self) -> None:
        """
        弹出文件保存对话框，并将表格数据保存为 CSV 或 JSON 格式。

        根据用户选择的文件类型，将数据保存为相应格式。保存成功后更新状态标签，失败则显示警告消息。

        :return: None
        """
        try:
            data = self.extract_table_data()
            if data is None:
                message_show('Critical', self.lang['ui.action_save_8'])
                return

            options = QFileDialog.Options()
            file_name, file_type = QFileDialog.getSaveFileName(self.main_window, self.lang['ui.action_save_3'], "", "CSV Files (*.csv);;JSON Files (*.json)", options=options)
            if not file_name:
                return

            if "csv" in file_type.lower():
                save_result = write_dict_to_csv(file_name, list(data.values()))
            elif "json" in file_type.lower():
                save_result = write_dict_to_json(file_name, data)
            else:
                save_result = None

            if save_result:
                self.label_status.setText(self.lang['ui.action_save_5'])
            else:
                message_show('Critical', self.lang['ui.action_save_7'])
        except Exception:
            logger.exception(f"Error saving file")
            self.label_status.setText(self.lang['label_status_error'])
