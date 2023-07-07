#! /usr/bin/env python

"""
/******************************************************************************
pip install requests
pip install PyCryptodome
代发查询
******************************************************************************/
"""
import json
import time

import requests
import hashlib
import base64
import hmac
import config
import hashlib
import base64
import hmac


def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


def send_notify(content):
    timestamp = str(round(time.time()))
    sign = gen_sign(timestamp, config.secret_string)
    msg_type = "text"
    at = '''<at user_id="all">所有人</at>'''
    content = {"text": content + at}
    msg = {"timestamp": timestamp, "sign": sign, "msg_type": msg_type, "content": content}
    r = requests.post(config.url, data=json.dumps(msg))
    return r


if __name__ == '__main__':
    send_notify('价格提醒')
