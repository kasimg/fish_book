"""
Created by kasim on 2019/7/9 12:53
"""

from flask import Flask
from flask_login import LoginManager
from app.models.base import db  # 此时db中已经包含表的信息
from flask_mail import Mail

"""
定义在这里的变量和函数可以直接用from 包名 import 变量/函数 直接引用
相当于变量和函数属于这个包

定义初始化操作，并向程序入口提供一个接口
"""

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__, static_folder='static')  # 初始化flask对象 这里决定了服务器的根目录是app
    # 用from_object方式引入的变量必须全部大写，否则读取时会忽略，导致后面取不到这个变量
    app.config.from_object('app.secure')  # 导入配置项
    app.config.from_object('app.setting')
    register_buleprint(app)  # 下面定义的函数

    db.init_app(app)  # 初始化db对象中的app
    # db.create_all(app=app)
    login_manager.init_app(app)  # 注册插件的初始化工作
    login_manager.login_view = 'web.login'  # 指定如果登录失败的话向哪里跳转
    login_manager.login_message = '请登录后重试！'
    # db.create_all(app=app)  # 利用模型创建表
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def register_buleprint(app):
    """
    注册蓝图
    :param app: app对象
    :return: 无
    """
    from app.web import web
    app.register_blueprint(web)
