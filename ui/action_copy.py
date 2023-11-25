"""
此模块提供了用于处理表格数据复制功能的类。

提供的类 `ActionCopy` 封装了与数据复制相关的所有操作，包括初始化界面、更新语言设置以及执行复制动作。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional, List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QTableWidgetSelectionRange, QTableWidget

from lib.get_resource_path import get_resource_path
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionCopy(QObject):
    """
    实现表格数据的复制功能。

    此类用于在表格界面中提供复制操作，允许用户复制选中的表格数据。

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
        self.action_copy = QAction(QIcon(get_resource_path('media/icons8-copy-26.png')), 'Copy')
        self.action_copy.setShortcut('Ctrl+C')
        self.action_copy.triggered.connect(self.copy_selected)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_copy.setText(self.lang['ui.action_copy_1'])
        self.action_copy.setStatusTip(self.lang['ui.action_copy_2'])

    def copy_selected(self) -> Optional[str]:
        """
        执行复制选中的表格数据。

        获取选中的表格范围，并将其中的数据格式化后复制到剪贴板。

        :rtype: Optional[str]
        :return: 复制的数据字符串，如果没有选中任何内容，则返回 None。
        """
        try:
            selected_ranges = self.table.selectedRanges()
            if not selected_ranges:
                return None

            clipboard_data = self._format_selected_data(selected_ranges)
            QApplication.clipboard().setText(clipboard_data)
            logger.info(f"Data copied, size: {len(clipboard_data)}")
            return clipboard_data
        except Exception:
            logger.exception("Error during copying")
            self.status_updated.emit(self.lang['label_status_error'])
            return None

    def _format_selected_data(self, selected_ranges: List[QTableWidgetSelectionRange]) -> str:
        """
        格式化选中的数据为字符串。

        遍历选中的每个区域，提取并格式化数据。

        :param selected_ranges: 选中的表格区域列表。
        :type selected_ranges: List[QTableWidgetSelectionRange]
        :rtype: str
        :return: 格式化后的数据字符串。
        """
        return '\n'.join(
            data for selected_range in selected_ranges
            for data in self._extract_range_data(selected_range)
        ).strip()

    def _extract_range_data(self, selected_range: QTableWidgetSelectionRange) -> List[str]:
        """
        提取选中区域的数据。

        对给定的表格区域，按行提取数据。

        :param selected_range: 选中的表格区域。
        :type selected_range: QTableWidgetSelectionRange
        :rtype: List[str]
        :return: 提取的行数据列表。
        """
        return [
            '\t'.join(self._extract_row_data(row, selected_range))
            for row in range(selected_range.topRow(), selected_range.bottomRow() + 1)
            if not self.table.isRowHidden(row)
        ]

    def _extract_row_data(self, row: int, selected_range: QTableWidgetSelectionRange) -> List[str]:
        """
        提取指定行的数据。

        对给定行和列范围，提取每个单元格的文本。

        :param row: 行号。
        :type row: int
        :param selected_range: 选中的表格区域。
        :type selected_range: QTableWidgetSelectionRange
        :rtype: List[str]
        :return: 提取的单元格数据列表。
        """
        return [
            self.table.item(row, col).text() if self.table.item(row, col) else ''
            for col in range(selected_range.leftColumn(), selected_range.rightColumn() + 1)
            if not self.table.isColumnHidden(col)
        ]
