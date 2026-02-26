"""
-*- coding: utf-8 -*-
@File: main.py
@author: WangZixu
"""

import os
import time

import config
from CodemaoEDUTools.api import PostAPI, DeleteAPI
from CodemaoEDUTools.user import GetUserToken

# 登录编程猫账号

token = GetUserToken(os.environ["CODEMAO_PHONE"], os.environ["CODEMAO_PASSWORD"])

# 获取顶帖ID列表

postnum = len(config.postid_list)

if postnum == 0:
    print("暂未填写顶帖ID，请在config.py内填写！")
    exit(1)
else:
    print(f"准备开始顶帖，共{postnum}个")
    success = 0
    all = 0

# 开始顶帖

for postid in config.postid_list:
    status = False
    # 发评论
    response = PostAPI(Path=f"/web/forums/posts/{postid}/replies", PostData={"content": config.postmsg}, Token=token)
    if response.status_code == 201:
        status = True
        replyid = response.json().get("id")
        print(f"{postid} 评论发送完毕")
    else:
        print(f"发生错误: ({response.status_code}) {response.text} | {postid}")

    # 删除评论
    if status:
        delete_response = DeleteAPI(Path=f"/web/forums/replies/{replyid}", Token=token)
        if delete_response.status_code == 204:
            success += 1
            all += 1
            print(f"{postid} 顶帖完成")
        else:
            print(f"发生错误: ({response.status_code}) {response.text} | {postid}")
            all += 1

    if all != len(config.postid_list):
        print("等待30s再进行下一个顶帖...")
        time.sleep(30)  # 访问限制

# 结束

print(f"顶帖已完成~ 共{postnum}个 成功{success}个")
