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
        """
        执行选定内容的复制操作。

        此方法触发复制选定范围的表格数据到剪贴板的流程。若没有选定的范围，则不进行任何操作。

        :return: 复制到剪贴板的文本数据，如果没有数据被复制，则返回 None。
        :rtype: Optional[str]
        """
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
        """
        格式化选定范围的表格数据为字符串。

        该方法遍历所有选定的表格区域，将数据转换为文本格式。

        :param selected_ranges: 选定的表格区域列表。
        :type selected_ranges: List[QTableWidgetSelectionRange]
        :return: 格式化后的字符串，用于复制到剪贴板。
        :rtype: str
        """
        rows_data = []
        for selected_range in selected_ranges:
            rows_data.extend(self._extract_range_data(selected_range))
        return '\n'.join(rows_data).strip()

    def _extract_range_data(self, selected_range: QTableWidgetSelectionRange) -> List[str]:
        """
        从选定的表格区域中提取数据。

        此方法遍历选定区域内的每一行，如果行未被隐藏，则调用 `_extract_row_data` 方法来获取该行的数据。

        :param selected_range: 用户在表格中选定的区域。
        :type selected_range: QTableWidgetSelectionRange
        :return: 选定区域中每行的数据组成的列表。
        :rtype: List[str]
        """
        range_data = []
        for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
            if not self.table.isRowHidden(row):
                range_data.append('\t'.join(self._extract_row_data(row, selected_range)))
        return range_data

    def _extract_row_data(self, row: int, selected_range: QTableWidgetSelectionRange) -> List[str]:
        """
        从表格的指定行中提取数据。

        此方法遍历指定行内的每一列，如果列未被隐藏，则获取该单元格的文本。

        :param row: 指定要提取数据的行号。
        :type row: int
        :param selected_range: 用户在表格中选定的区域。
        :type selected_range: QTableWidgetSelectionRange
        :return: 指定行中每个单元格的数据组成的列表。
        :rtype: List[str]
        """
        row_data = []
        for col in range(selected_range.leftColumn(), selected_range.rightColumn() + 1):
            if not self.table.isColumnHidden(col):
                cell_text = self.table.item(row, col).text() if self.table.item(row, col) else ''
                row_data.append(cell_text)
        return row_data
