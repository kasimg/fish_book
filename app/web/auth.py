from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from wtforms import ValidationError

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('web.login'))  # redirect需要return，否则不会跳转
    except ValidationError as v:
        return '电子邮件已被注册'
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)  # 写入的是一次性cookie
            next = request.args.get('next')
            if not next or not next.startswith('/'):  # 如果next不是以/开头，为了防止重定向攻击，需要强行转向首页
                next = url_for('web.index')  # 如何找到首页？url_for后面跟的都是视图函数？
            return redirect(next)  # redirect需要return，否则不会跳转
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            from app.libs.email import send_email
            send_email(form.email.data, '重置你的密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash('重置密码邮件已发送到邮箱' + account_email + ', 请及时查收')
            # return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('密码已更新，请重新登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()  # 清除浏览器cookie
    return redirect(url_for('web.index'))
