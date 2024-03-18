import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
"""
这段代码的功能是获取当前文件的父目录的绝对路径。
1. 导入os模块。
2. 使用os.path.dirname(__file__)获取当前文件的目录路径。
3. 使用os.path.dirname()再次获取当前文件的父目录路径。
4. 使用os.path.abspath()将父目录路径转换为绝对路径。
5. 将绝对路径赋值给变量basedir。
"""


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'aswunxqkxqlxnwza;lf')
    # 定义一个名为SECRET_KEY的变量，并将其值设置为环境变量中的"SECRET_KEY"，如果环境变量中没有设置该值，则将其默认值设置为"secret string"。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOG_EMAIL = os.getenv("EMAIL")
    BLOG_POST_PER_PAGE = 10
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15

    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "2368996924@qq.com"
    MAIL_PASSWORD = "huxyljfxunyuebic"
    MAIL_DEFAULT_SENDER = "2368996924@qq.com"

    CACHE_TYPE = 'redis'


"""这段代码的作用是设置一些常量值。
代码通过调用 `os.getenv()` 方法获取名为"BLOG_EMAIL"的环境变量的值，并将其赋给常量 `BLOG_EMAIL` 。
接下来，代码设置了三个常量值：
BLOG_POST_PER_PAGE` 的值为10，表示每页显示10篇博文。
BLOG_MANAGE_POST_PER_PAGE` 的值为15，表示在管理页面每页显示15篇博文。
BLOG_COMMENT_PER_PAGE` 的值为15，表示每页显示15条评论。
"""


class DevelopmentConfig(BaseConfig):
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'blog2'
    USERNAME = 'root'
    PASSWORD = 'root'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI


class TestingConfig(BaseConfig):
    TESTING = True
    WTE_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-dev.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
