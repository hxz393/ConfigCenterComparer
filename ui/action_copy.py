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

# 初始化日志记录器
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
        复制所选内容到剪贴板。

        此方法获取表格中用户所选的区域，并将其内容复制到剪贴板。

        :rtype: Optional[str]
        :return: 复制到剪贴板的文本内容，如果发生异常则返回 None。
        """
        try:
            selected_ranges = self.table.selectedRanges()
            if not selected_ranges:
                return None

            clipboard_data = self._format_selected_data(selected_ranges)
            clipboard = QApplication.clipboard()
            clipboard.setText(clipboard_data)
            return clipboard_data
        except Exception:
            logger.exception(f"Error during copying")
            self.label_status.setText(self.lang['label_status_error'])

    def _format_selected_data(self, selected_ranges: List[QTableWidgetSelectionRange]) -> str:
        """
        格式化所选区域的数据为字符串。

        此方法负责将用户在表格中选中的数据区域转换为文本格式，以便复制到剪贴板。

        :type selected_ranges: List[QTableWidgetSelectionRange]
        :param selected_ranges: 选中的区域列表，每个区域是一个 QTableWidgetSelectionRange 对象。
        :rtype: str
        :return: 格式化后的字符串。
        """
        rows_data = []
        for selected_range in selected_ranges:
            for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
                if not self.table.isRowHidden(row):
                    row_data = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(selected_range.leftColumn(), selected_range.rightColumn() + 1)]
                    rows_data.append('\t'.join(row_data))
        return '\n'.join(rows_data).strip()
