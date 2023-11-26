"""
这个模块提供了一个全局信号类，用于管理不同组件间的信号通信。

GlobalSignals 类是 PyQt5 的信号封装，用于在应用程序的不同部分之间发送通知。它可以用于触发对话框关闭、数据更新等事件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

from PyQt5.QtCore import QObject, pyqtSignal


class GlobalSignals(QObject):
    """
    这个类提供了一个用于发送全局信号的机制。

    GlobalSignals 类使用 PyQt5 的 QObject 和 pyqtSignal 来创建自定义信号。这些信号可以在整个应用程序中使用，以实现组件间的通信。

    :example:
    >>> global_signals = GlobalSignals()
    >>> global_signals.close_all.connect(some_function)
    在这个例子中，当 close_dialog 信号被触发时，会调用 some_function 函数。
    """

    close_all = pyqtSignal()


# 创建全局信号的单一实例
global_signals = GlobalSignals()