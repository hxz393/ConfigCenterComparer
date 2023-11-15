"""
这是一个Python文件，其中包含一个函数：`request_url`。

函数 `request_url` 用于通过 HTTP GET 请求获取给定 URL 的响应内容。它接受一个参数 `url`，这是需要请求的URL。函数首先创建一个requests.Session对象，然后发送一个GET请求到 `url`。如果响应的状态码是200，函数将返回响应的内容，否则返回 `None`。在发生网络请求异常时，函数将记录错误并返回 `None`。

此模块主要用于发送HTTP GET请求并处理可能的异常。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

import requests

requests.packages.urllib3.disable_warnings()
logger = logging.getLogger(__name__)


def request_url(url: str) -> Optional[str]:
    """
    通过 HTTP GET 请求获取给定 URL 的响应内容。

    :param url: 待请求的 URL
    :type url: str

    :rtype: Optional[str]
    :return: 如果请求成功，返回 URL 的响应内容；否则返回 None
    """
    session = requests.Session()
    session.trust_env = False

    try:
        response = session.get(url, verify=False, timeout=15)
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        logger.exception(f"Unable to send network request to {url}")
        return None
