"""
这是一个用于显示软件相关信息的对话框模块。

此模块包含一个 `DialogAbout` 类，用于创建并显示关于软件的信息，如版本号、作者、网址链接等。它通过 PyQt5 构建用户界面，提供一个图形化的方式来展示软件信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFormLayout, QTextEdit

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import VERSION_INFO, GITHUB_URL, PROGRAM_NAME, WEBSITE_URL, AUTHOR_NAME
from lib.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


class DialogAbout(QDialog):
    """
    创建并显示关于软件的信息对话框。

    此类使用 PyQt5 构建用户界面，展示软件名称、版本、作者信息等。

    :param main_window: 主窗口对象，用于获取语言和状态栏信息。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化对话框，并设置基本属性。

        :param main_window: 主窗口对象，用于获取语言和状态栏信息。
        :type main_window: ConfigCenterComparer
        """
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.main_window = main_window
        self.lang = self.main_window.get_elements('lang')
        self.label_status = self.main_window.get_elements('label_status')

        self.setWindowTitle(self.lang['ui.dialog_about_1'])
        self.setFixedSize(463, 470)
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-about-26.png')))
        self.setStyleSheet("font-size: 14px;")

        self.initUI()

    def initUI(self):
        """
        初始化用户界面组件。

        创建对话框中的所有UI元素，并进行布局。
        """
        try:
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            # 构建显示区域
            layout.addWidget(self._create_top_area())
            layout.addLayout(self._create_middle_area())
            layout.addWidget(self._create_bottom_area())

            self.setLayout(layout)
        except Exception:
            logger.exception(f"Failed to initialize DialogAbout")
            self.label_status.setText(self.lang['label_status_error'])

    def _create_top_area(self) -> QWidget:
        """
        创建对话框顶部区域。

        :return: 包含顶部区域的QWidget对象。
        :rtype: QWidget
        """
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        # 程序图标
        image = QLabel()
        image.setContentsMargins(20, 10, 20, 10)
        image.setPixmap(QPixmap(get_resource_path("media/main.ico")))
        top_layout.addWidget(image)
        # 名称和版本信息
        top_layout.addLayout(self._title_and_version())
        top_layout.addStretch()
        # 设置背景颜色
        widget = QWidget()
        widget.setStyleSheet("background-color: white;")
        widget.setLayout(top_layout)

        return widget

    def _title_and_version(self) -> QVBoxLayout:
        """
        创建对话框标题和版本信息区域。

        :return: 包含标题和版本信息的QVBoxLayout对象。
        :rtype: QVBoxLayout
        """
        layout = QVBoxLayout()
        # 大标题
        title = QLabel(PROGRAM_NAME)
        title.setContentsMargins(0, 10, 20, 0)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)
        # 描述文字
        name = QLabel(self.lang['ui.dialog_about_2'])
        name.setContentsMargins(0, 20, 0, 0)
        layout.addWidget(name)
        # 版本信息
        version = QLabel(f"{self.lang['ui.dialog_about_3']}{VERSION_INFO}")
        version.setContentsMargins(0, 0, 0, 10)
        layout.addWidget(version)

        return layout

    def _create_middle_area(self) -> QFormLayout:
        """
        创建对话框中间区域。

        :return: 包含中间区域的QFormLayout对象。
        :rtype: QFormLayout
        """
        # 多行内容
        infos = {
            self.lang['ui.dialog_about_4']: AUTHOR_NAME,
            self.lang['ui.dialog_about_5']: WEBSITE_URL,
            self.lang['ui.dialog_about_6']: GITHUB_URL
        }
        # 表单布局
        layout = QFormLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(10)
        # 插入表单
        for k, v in infos.items():
            title = QLabel(k)
            title.setStyleSheet("font-weight: bold;")
            info = QLabel(f"<a href='{v}'>{v}</a>")
            info.setTextFormat(Qt.RichText)
            info.setTextInteractionFlags(Qt.TextBrowserInteraction)
            info.setOpenExternalLinks(True)
            layout.addRow(title, info)

        return layout

    def _create_bottom_area(self) -> QTextEdit:
        """
        创建对话框底部区域。

        :return: 包含底部区域的QTextEdit对象。
        :rtype: QTextEdit
        """
        # 说明信息
        info = QTextEdit()
        info.setHtml(self.lang['ui.dialog_about_7'])
        info.setReadOnly(True)

        return info
