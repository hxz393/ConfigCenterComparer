"""
本文件定义了一个关于对话框的类 `DialogAbout`，用于在 PyQt5 框架中显示关于程序的信息。

该类包括初始化界面、更新语言设置、创建顶部、中间、底部区域等方法。通过这些方法，可以构建一个包含程序信息、版本号、作者信息等的对话框。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFormLayout, QTextEdit

from config.settings import VERSION_INFO, GITHUB_URL, GITHUB_PROFILE, PROGRAM_NAME, WEBSITE_URL, AUTHOR_NAME
from lib.get_resource_path import get_resource_path
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class DialogAbout(QDialog):
    """
    `DialogAbout` 类用于创建关于对话框，展示程序的相关信息。

    :param lang_manager: 语言管理器，用于更新动作的显示语言。
    :type lang_manager: LangManager
    """

    def __init__(self, lang_manager: LangManager):
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.lang_manager = lang_manager
        self.lang = self.lang_manager.get_lang()
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.setWindowTitle(self.lang['ui.dialog_about_1'])
        self.setFixedSize(463, 470)
        self.setWindowIcon(QIcon(get_resource_path('media/main.svg')))
        self.setStyleSheet("font-size: 14px;")
        # 竖向布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # 构建显示区域
        layout.addWidget(self._create_top_area())
        layout.addLayout(self._create_middle_area())
        layout.addWidget(self._create_bottom_area())

        self.setLayout(layout)

    def _create_top_area(self) -> QWidget:
        """
        创建对话框顶部区域。

        :return: 包含顶部区域的QWidget对象。
        :rtype: QWidget
        """
        # 横向布局
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # 程序图标
        layout.addWidget(self._clickable_image())
        # 名称和版本信息
        layout.addLayout(self._title_and_version())
        layout.addStretch()
        # 设置背景颜色
        widget = QWidget()
        widget.setStyleSheet("background-color: white;")
        widget.setLayout(layout)

        return widget

    @staticmethod
    def _clickable_image() -> QLabel:
        """
        创建图片组件，用于存放处理过的 SVG 图像。

        :return: 包含程序大图标。
        :rtype: QLabel
        """
        # 创建 QLabel 用于显示图像
        label = QLabel()
        label.setContentsMargins(20, 10, 10, 10)

        # 加载 SVG 文件并调整大小
        pixmap = QPixmap(96, 96)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        QSvgRenderer(get_resource_path("media/main.svg")).render(painter)
        painter.end()

        # 将 pixmap 转换为 base64 编码的字符串
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        base64_data = byte_array.toBase64().data().decode()

        # 设置 HTML 链接和图像
        html = f"<a href='{GITHUB_PROFILE}'><img src='data:image/png;base64,{base64_data}' /></a>"
        label.setText(html)
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)

        return label

    def _title_and_version(self) -> QVBoxLayout:
        """
        创建对话框标题和版本信息区域。

        :return: 包含标题和版本信息的QVBoxLayout对象。
        :rtype: QVBoxLayout
        """
        # 竖向布局
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
        version.setStyleSheet("font-weight: bold; text-align: center;")
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
            # 左列标题
            title = QLabel(k)
            title.setStyleSheet("font-weight: bold;")
            # 右列信息，超链接
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
