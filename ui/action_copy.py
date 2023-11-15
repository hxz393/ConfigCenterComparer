"""
这是一个用于配置中心比较器的辅助模块，主要包含复制功能的实现。

此模块中的主要类为 `ActionCopy`，它封装了与复制操作相关的逻辑。类提供了用户界面交互功能，允许用户复制选定的表格数据到剪贴板。此外，模块也包括必要的错误处理和日志记录。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QTableWidgetSelectionRange

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)

class ActionCopy:
    """
    处理配置中心比较器中的复制动作的类。

    此类封装了复制操作的界面逻辑，包括初始化复制菜单项、绑定相关事件、以及执行复制动作。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化复制动作。

        :param main_window: 配置中心比较器的主窗口对象。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_copy = QAction(QIcon(get_resource_path('media/icons8-copy-26.png')), self.lang['ui.action_copy_1'], self.main_window)
        self.action_copy.setShortcut('Ctrl+C')
        self.action_copy.setStatusTip(self.lang['ui.action_copy_2'])
        self.action_copy.triggered.connect(self.copy_selected)

    def copy_selected(self) -> Optional[str]:
        try:
            selected_ranges = self.table.selectedRanges()
            if not selected_ranges:
                return None

            clipboard_data = self._format_selected_data(selected_ranges)
            QApplication.clipboard().setText(clipboard_data)
            return clipboard_data
        except Exception:
            logger.exception("Error during copying")
            self.label_status.setText(self.lang['label_status_error'])
            return None

    def _format_selected_data(self, selected_ranges: List[QTableWidgetSelectionRange]) -> str:
        rows_data = []
        for selected_range in selected_ranges:
            rows_data.extend(self._extract_range_data(selected_range))
        return '\n'.join(rows_data).strip()

    def _extract_range_data(self, selected_range: QTableWidgetSelectionRange) -> List[str]:
        range_data = []
        for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
            if not self.table.isRowHidden(row):
                range_data.append('\t'.join(self._extract_row_data(row, selected_range)))
        return range_data

    def _extract_row_data(self, row: int, selected_range: QTableWidgetSelectionRange) -> List[str]:
        row_data = []
        for col in range(selected_range.leftColumn(), selected_range.rightColumn() + 1):
            if not self.table.isColumnHidden(col):
                cell_text = self.table.item(row, col).text() if self.table.item(row, col) else ''
                row_data.append(cell_text)
        return row_data
