"""
Created by kasim on 2019/7/9 13:50
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(Form):
    """
    书本查询参数的验证类
    """
    # 定义验证规则，validators是数组，可以传入多个参数
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)