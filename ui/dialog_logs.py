"""
这是一个用于展示和处理应用程序日志的模块。

此模块包含`DialogLogs`类，用于在图形用户界面中显示和过滤应用程序的日志。它允许用户根据日志级别进行筛选，并提供清除日志的功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import re
import webbrowser
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor, QIcon
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox, QLabel, QWidget

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import GITHUB_URL, LOG_PATH
from lib.get_resource_path import get_resource_path
from lib.write_list_to_file import write_list_to_file

logger = logging.getLogger(__name__)


class DialogLogs(QDialog):
    """
    用于展示和处理应用程序日志的对话框类。

    此类提供一个图形界面，用于显示和过滤应用程序的日志信息。它允许用户根据日志级别筛选日志，并提供清除日志的功能。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    :param parent: 父窗口对象。
    :type parent: Optional[QWidget]
    """
    LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    LOG_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - (DEBUG|INFO|WARNING|ERROR|CRITICAL) - ')

    def __init__(self, main_window: ConfigCenterComparer, parent: Optional[QWidget] = None):
        """
        初始化日志对话框。

        此方法初始化对话框界面，包括日志文本编辑器、筛选下拉框和操作按钮。

        :param main_window: 配置中心比较器的主窗口对象。
        :type main_window: ConfigCenterComparer
        :param parent: 父窗口对象，可选。
        :type parent: Optional[QWidget]
        """
        super().__init__(parent, flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.setWindowTitle(self.lang['ui.dialog_logs_1'])
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-log-26.png')))
        self.resize(600, 470)

        # 创建日志文本编辑器，设置为只读，不换行
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)

        # 创建标签和下拉框
        self.label = QLabel(self.lang['ui.dialog_logs_2'], self)
        self.combo_box = QComboBox(self)
        self.combo_box.addItem(self.lang['ui.dialog_logs_3'], None)
        self.combo_box.addItems(DialogLogs.LEVELS)
        self.combo_box.currentIndexChanged.connect(self.filter_logs)

        # 创建按钮
        feedback_button = QPushButton(self.lang['ui.dialog_logs_4'], self)
        feedback_button.clicked.connect(self.open_github)
        clear_button = QPushButton(self.lang['ui.dialog_logs_5'], self)
        clear_button.clicked.connect(self.clear_logs)
        close_button = QPushButton(self.lang['ui.dialog_logs_6'], self)
        close_button.clicked.connect(self.close)

        # 布局设置
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label)
        top_layout.addWidget(self.combo_box)
        top_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addWidget(feedback_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

        self._load_logs()

    def _load_logs(self) -> None:
        """
        加载并处理日志文件。

        此方法读取日志文件的内容，并根据当前的筛选级别显示日志信息。
        """
        try:
            logs_content = self._read_logs_file()
            self._process_logs(logs_content)
        except Exception:
            logger.exception("Open log file error")
            logger.exception("Error opening log file")
            self.label_status.setText(self.lang['label_status_error'])

    def clear_logs(self) -> None:
        """
        清除日志显示。

        此方法清空文本编辑器中的日志，并清空日志文件。
        """
        try:
            self.text_edit.clear()
            write_list_to_file(LOG_PATH, [])
        except Exception:
            logger.exception("Error clearing logs")
            self.label_status.setText(self.lang['label_status_error'])

    @staticmethod
    def _read_logs_file() -> str:
        """
        读取日志文件内容。

        此方法从日志文件中读取所有日志内容并返回。

        :return: 日志文件的内容。
        :rtype: str
        """
        try:
            with open(LOG_PATH, 'r', encoding='utf8') as file:
                return file.read()
        except Exception:
            logger.exception("Error reading log file")
            return ""

    def _process_logs(self, logs_content: str, filter_level: Optional[str] = None) -> None:
        """
        处理并显示日志。

        此方法将日志内容按照指定的过滤级别进行处理，并显示在文本编辑器中。

        :param logs_content: 完整的日志内容。
        :type logs_content: str
        :param filter_level: 要筛选的日志级别，可选。
        :type filter_level: Optional[str]
        """
        start_positions = [match.start() for match in DialogLogs.LOG_PATTERN.finditer(logs_content)]

        for i in range(len(start_positions)):
            start = start_positions[i]
            end = start_positions[i + 1] if i + 1 < len(start_positions) else None
            log_entry = logs_content[start:end]
            if filter_level is None or self._is_log_entry_of_level(log_entry, filter_level):
                self._parse_and_display_log(log_entry)

    def _parse_and_display_log(self, log_entry: str) -> None:
        """
        解析并显示单条日志。

        此方法解析单条日志信息，并以适当的颜色显示在文本编辑器中。

        :param log_entry: 单条日志的内容。
        :type log_entry: str
        """
        match = DialogLogs.LOG_PATTERN.search(log_entry)
        if match:
            log_level = match.group(1)
            color = self._get_color_for_level(log_level)
        else:
            color = "black"
        self._append_log(log_entry, color)

    def filter_logs(self) -> None:
        """
        根据选定级别过滤日志。

        此方法根据用户在下拉框中选择的日志级别筛选日志。
        """
        try:
            selected_level = self.combo_box.currentText()
            self.text_edit.clear()
            logs_content = self._read_logs_file()
            self._process_logs(logs_content, selected_level)
        except Exception:
            logger.exception("Error filtering logs")
            self.label_status.setText(self.lang['label_status_error'])

    def _append_log(self, log: str, color: str) -> None:
        """
        将日志添加到文本编辑器。

        此方法将指定颜色的日志文本添加到文本编辑器中。

        :param log: 要添加的日志文本。
        :type log: str
        :param color: 日志文本的颜色。
        :type color: str
        """
        color_format = QTextCharFormat()
        color_format.setForeground(QColor(color))

        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(log, color_format)

    @staticmethod
    def _get_color_for_level(level: str) -> str:
        """
        获取日志级别对应的颜色。

        此方法根据日志级别返回相应的颜色字符串。

        :param level: 日志级别。
        :type level: str
        :return: 对应日志级别的颜色。
        :rtype: str
        """
        colors = {
            "DEBUG": "gray",
            "INFO": "black",
            "WARNING": "orange",
            "ERROR": "red",
            "CRITICAL": "darkred"
        }
        return colors.get(level, "black")

    #

    def _is_log_entry_of_level(self, log_entry: str, selected_level: str) -> bool:
        """
        判断日志条目是否为选定级别。

        此方法检查日志条目是否为或高于用户选定的日志级别。

        :param log_entry: 单条日志的内容。
        :type log_entry: str
        :param selected_level: 选定的日志级别。
        :type selected_level: str
        :return: 日志条目是否为选定级别。
        :rtype: bool
        """
        if selected_level == self.lang['ui.dialog_logs_3']:
            return True
        selected_index = DialogLogs.LEVELS.index(selected_level)
        for level in DialogLogs.LEVELS[selected_index:]:
            if f' - {level} - ' in log_entry:
                return True
        return False

    @staticmethod
    def open_github() -> None:
        """
        打开GitHub问题页面。

        此方法在用户点击反馈按钮时，打开GitHub的问题跟踪页面。
        """
        webbrowser.open(f'{GITHUB_URL}/issues')
