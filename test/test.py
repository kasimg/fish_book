"""
Created by kasim on 2019/7/10 9:18
"""
from flask import Flask, current_app, Request

app = Flask(__name__)

# 上下文表达式需要返回一个对象，对象中实现了__enter__ 和 __exit__方法
# 才能使用with
with app.app_context():
    a = current_app
    c = current_app._get_current_object()
    d = current_app.config['DEBUG']

print(11)
# ctx.pop()
