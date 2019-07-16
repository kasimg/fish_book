"""
Created by kasim on 2019/7/12 9:41
"""
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    nickname = StringField('nickname', validators=[
        DataRequired(message='请输入昵称！'),
        Length(2, 10, message='昵称至少需要两个字符，最多10个字符')
    ])

    password = PasswordField('password', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'),
        Length(6, 32, message='密码的长度需要在6-32位之间')
    ])

    email = StringField('email', validators=[
        DataRequired(message='请输入邮箱！！'),
        Length(8, 64, '电子邮件长度不符合规范'),
        Email(message='电子邮件格式不符合规范')
    ])

    def validate_email(self, field):
        """
        注意命名规则，validate_email 下划线后面跟上需要校验的属性
        不需要在属性后面的validators中再次加入自定义校验器
        :param field:
        :return:
        """
        r = User.query.filter_by(email=field.data).first()
        if r:
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        """
        注意命名规则，validate_email 下划线后面跟上需要校验的属性
        不需要在属性后面的validators中再次加入自定义校验器
        :param field:
        :return:
        """
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已被注册')


class EmailForm(Form):
    email = StringField('email', validators=[
        DataRequired(message='请输入邮箱！！'),
        Length(8, 64, '电子邮件长度不符合规范'),
        Email(message='电子邮件格式不符合规范')])


class LoginForm(EmailForm):
    password = PasswordField('password', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'),
        Length(6, 32, message='密码的长度需要在6-32位之间')
    ])


class ResetPasswordForm(Form):
    password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 20)])

# email = StringField('email', validators=[
#     DataRequired(message='请输入邮箱！！'),
#     Length(8, 64, '电子邮件长度不符合规范'),
#     Email(message='电子邮件格式不符合规范')])
