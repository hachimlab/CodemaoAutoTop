"""
用户
"""

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from .api import PostAPI, PostWithoutTokenAPI

logger = logging.getLogger(__name__)


def GetUserToken(Username: str, Password: str) -> str | bool:
    """登录并获取用户Token"""
    response = PostWithoutTokenAPI(
        Path="/tiger/v3/web/accounts/login",
        PostData={"pid": "65edCTyg", "identity": Username, "password": Password},
    )
    if response.status_code == 200:
        return str(json.loads(response.text).get("auth", {}).get("token"))
    else:
        logger.error(
            f"请求失败，用户名：{Username}, 状态码: {response.status_code}, 响应: {response.text[:100]}"
        )
        return False