# -*- coding: utf-8 -*-

import requests
import time
import re

tip = 0


def get_uuid():

    url = 'https://login.weixin.qq.com/jslogin'
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
        'lang': 'zh_CN',
        '_': int(time.time()),
    }
    response = requests.get(url=url, params=params)
    data = response.text

    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, data)

    code = pm.group(1)
    uuid = pm.group(2)

    if code == '200':
        return uuid

    return None


def qr_image():
    url = 'https://login.weixin.qq.com/qrcode/' + uuid
    params = {
        't': 'webwx',
        '_': int(time.time()),
    }

    response = requests.get(url, params=params)
    return


if __name__ == '__main__':
    uuid = get_uuid()
    qr_image()
