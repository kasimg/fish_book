"""
Created by kasim on 2019/7/8 19:30
存放机密信息
git ignore掉
"""
DEBUG = False

#  数据库连接信息机密信息，需要放在此处
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:wjdh88166016@localhost:3306/fish_book'

SECRET_KEY = 'ASDF93W49DSFYDV79498USDYF984W987SD8YFASHWER'

# Email配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'guoyanghaoren@qq.com'
MAIL_PASSWORD = 'cfzvxkxsppmybejh'
