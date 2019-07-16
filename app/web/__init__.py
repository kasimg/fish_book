"""
Created by kasim on 2019/7/9 12:56
"""
from flask import Blueprint, render_template

web = Blueprint('web', __name__)  # 初始化蓝图对象，在app初始化时导出用于注册蓝图

@web.app_errorhandler(404)
def not_found(e):
    """
    AOP思想，把可能出现404的情况放到一起处理
    :param e:
    :return:
    """
    return render_template('404.html'), 404

# 注册视图函数，不能写在蓝图初始化之前
# 否则book在导入web变量时web还未定义
from . import book  # 执行book中的代码
from . import auth
from . import drift
from . import gift
from . import main
from . import wish

from . import test
