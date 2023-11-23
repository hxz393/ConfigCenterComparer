"""
本模块提供了用于日志查看和管理的功能，包括日志显示、过滤、清除等。

此模块定义了 `DialogLogs` 类，用于创建和管理一个日志对话框界面。该界面允许用户查看应用程序的日志，
过滤显示特定级别的日志，以及清除日志内容。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import re
import webbrowser
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor, QIcon
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox, QLabel

from config.settings import GITHUB_URL, LOG_PATH, LOG_COLORS, LOG_DEFAULT_LEVEL, LOG_LINES, LOG_UPDATE_TIME
from lib.get_resource_path import get_resource_path
from lib.write_list_to_file import write_list_to_file
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class DialogLogs(QDialog):
    """
    日志对话框类，用于显示和管理应用程序的日志。

    此类创建一个对话框，显示应用程序的日志内容，并提供过滤、清除和实时更新日志的功能。

    :param lang_manager: 语言管理器，用于界面语言的国际化。
    :type lang_manager: LangManager
    """
    LOG_LEVELS = [i for i in LOG_COLORS.keys()]
    LOG_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - (DEBUG|INFO|WARNING|ERROR|CRITICAL) - ')
    status_updated = pyqtSignal(str)

    def __init__(self, lang_manager: LangManager):
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        # 设置对话框为非模态。或者设置标记 Qt.NonModal
        self.setModal(False)
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-log-26.png')))
        self.resize(600, 470)

        # 创建日志文本编辑器，设置为只读，不换行
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)

        # 创建标签和下拉框
        self.label = QLabel(self)
        self.combo_box = QComboBox(self)
        self.combo_box.addItem(LOG_DEFAULT_LEVEL, None)
        self.combo_box.addItems(DialogLogs.LOG_LEVELS)
        self.combo_box.currentIndexChanged.connect(self.filter_logs)

        # 创建按钮
        self.feedback_button = QPushButton(self)
        self.feedback_button.clicked.connect(self.open_github)
        self.clear_button = QPushButton(self)
        self.clear_button.clicked.connect(self.clear_logs)
        self.refresh_button = QPushButton(self)
        # 将按钮设置为可检查（切换状态）
        self.refresh_button.setCheckable(True)
        self.refresh_button.setStyleSheet("QPushButton{background-color: #DDD;}")
        self.refresh_button.clicked.connect(self.toggle_real_time_logs)
        self.close_button = QPushButton(self)
        self.close_button.clicked.connect(self.close)

        # 布局设置
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label)
        top_layout.addWidget(self.combo_box)
        top_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.feedback_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.close_button)

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

        # 初始化定时器，但不立即启动
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_logs)
        # 添加一个标记来追踪实时更新状态
        self.log_file_position = 0

        self.update_lang()
        self.load_logs()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.setWindowTitle(self.lang['ui.dialog_logs_1'])
        self.label.setText(self.lang['ui.dialog_logs_2'])
        self.feedback_button.setText(self.lang['ui.dialog_logs_4'])
        self.clear_button.setText(self.lang['ui.dialog_logs_5'])
        self.refresh_button.setText(self.lang['ui.dialog_logs_7'])
        self.close_button.setText(self.lang['ui.dialog_logs_6'])

    def load_logs(self) -> None:
        """
        加载并处理日志文件。

        读取日志文件的内容，并根据当前的筛选级别显示日志信息。

        :rtype: None
        :return: 无返回值。
        """
        try:
            self.text_edit.clear()
            logs_content = self._read_logs_file()
            self._process_logs(logs_content)
            self.text_edit.moveCursor(QTextCursor.End)
        except Exception:
            logger.exception("Error opening log file")
            self.status_updated.emit(self.lang['label_status_error'])

    def clear_logs(self) -> None:
        """
        清除日志显示。

        清空文本编辑器中的日志，并清空日志文件。

        :rtype: None
        :return: 无返回值。
        """
        try:
            self.text_edit.clear()
            write_list_to_file(LOG_PATH, [])
        except Exception:
            logger.exception("Error clearing logs")
            self.status_updated.emit(self.lang['label_status_error'])

    def update_logs(self) -> None:
        """
        更新日志内容。

        读取新的日志内容并追加到文本编辑器。

        :rtype: None
        :return: 无返回值。
        """
        try:
            with open(LOG_PATH, 'r', encoding='utf8') as file:
                # 移动到上次读取的位置
                file.seek(self.log_file_position)
                # 读取新内容
                new_content = file.read()
                # 更新读取位置
                self.log_file_position = file.tell()
            # 如果有新内容
            if new_content:
                self._process_logs(new_content)
                self.text_edit.moveCursor(QTextCursor.End)
        except Exception:
            logger.exception("Error updating logs")
            self.status_updated.emit(self.lang['label_status_error'])

    def toggle_real_time_logs(self) -> None:
        """
        切换实时日志更新功能，启用或禁用定时器。

        :rtype: None
        :return: 无返回值。
        """
        self.update_timer.start(LOG_UPDATE_TIME) if self.refresh_button.isChecked() else self.update_timer.stop()

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
                lines = file.readlines()
                # 获取最后的LOG_LINES行
                return ''.join(lines[-int(LOG_LINES):])
        except Exception:
            logger.exception("Error reading log file")
            return ""

    def _process_logs(self,
                      logs_content: str,
                      filter_level: Optional[str] = None) -> None:
        """
        处理并显示日志。

        将日志内容按照指定的过滤级别进行处理，并显示在文本编辑器中。

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

        解析单条日志信息，并以适当的颜色显示在文本编辑器中。

        :param log_entry: 单条日志的内容。
        :type log_entry: str
        """
        match = DialogLogs.LOG_PATTERN.search(log_entry)
        if match:
            log_level = match.group(1)
            color = LOG_COLORS.get(log_level, "black")
        else:
            color = "black"
        self._append_log(log_entry, color)

    def filter_logs(self) -> None:
        """
        根据选定级别过滤日志。

        根据用户在下拉框中选择的日志级别筛选日志。

        :rtype: None
        :return: 无返回值。
        """
        try:
            selected_level = self.combo_box.currentText()

            # 保存当前光标位置
            current_cursor = self.text_edit.textCursor()
            current_position = current_cursor.position()

            # 清除并重新加载日志
            self.text_edit.clear()
            logs_content = self._read_logs_file()
            self._process_logs(logs_content, selected_level)

            # 尝试恢复光标到之前的位置
            new_cursor = self.text_edit.textCursor()
            new_cursor.setPosition(min(current_position, len(self.text_edit.toPlainText())))
            self.text_edit.setTextCursor(new_cursor)
        except Exception:
            logger.exception("Error filtering logs")
            self.status_updated.emit(self.lang['label_status_error'])

    def _append_log(self,
                    log: str,
                    color: str) -> None:
        """
        将日志添加到文本编辑器。

        使用指定的颜色将单条日志文本添加到文本编辑器中。

        :param log: 要添加的日志文本。
        :type log: str
        :param color: 日志文本的颜色。
        :type color: str
        :rtype: None
        :return: 无返回值。
        """
        color_format = QTextCharFormat()
        color_format.setForeground(QColor(color))

        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(log, color_format)

    @staticmethod
    def _is_log_entry_of_level(log_entry: str,
                               selected_level: str) -> bool:
        """
        判断日志条目是否为选定级别。

        检查日志条目是否为或高于用户选定的日志级别。

        :param log_entry: 单条日志的内容。
        :type log_entry: str
        :param selected_level: 选定的日志级别。
        :type selected_level: str
        :return: 日志条目是否为选定级别。
        :rtype: bool
        """
        if selected_level == LOG_DEFAULT_LEVEL:
            return True
        selected_index = DialogLogs.LOG_LEVELS.index(selected_level)
        for level in DialogLogs.LOG_LEVELS[selected_index:]:
            if f' - {level} - ' in log_entry:
                return True
        return False

    def open_github(self) -> None:
        """
        打开GitHub问题页面。

        在用户点击反馈按钮时，打开GitHub的问题跟踪页面。

        :rtype: None
        :return: 无返回值。
        """
        try:
            webbrowser.open(f'{GITHUB_URL}/issues')
        except Exception:
            logger.exception("Failed to open GitHub URL")
            self.status_updated.emit(self.lang['label_status_error'])
