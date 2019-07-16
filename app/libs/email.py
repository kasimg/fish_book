"""
Created by kasim on 2019/7/16 14:45
"""
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except:
            pass

def send_email(to=None, subject=None, template=None, **kwargs):
    # msg = Message('测试邮件', sender='guoyanghaoren@qq.com', body='test',
    #               recipients=['guoyanghaoren@qq.com'])
    msg = Message('[鱼书] ' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()  # 获取真实的核心对象
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    # mail.send(msg)