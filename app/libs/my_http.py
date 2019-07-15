"""
Created by kasim on 2019/7/9 9:15
"""
import requests


class HTTP:
    """
    用来发送http请求的类
    """
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text