# 扩展类实例化

from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

bootstrap = Bootstrap4()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
ckeditor = CKEditor()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from commons.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

# 1. `@login_manager.user_loader` 这部分代码是一个装饰器，用于对使用 Flask-Login 的用户加载函数进行设置。在这里，`user_loader` 装饰器会告诉 Flask-Login
# 如何加载用户对象。当用户登录后，Flask-Login 将使用这个装饰的函数来加载与用户 ID 相关联的用户对象。 举例来说，假设一个用户在登录后，通过 `load_user` 函数来加载与用户 ID
# 相关联的用户对象。这个函数从数据库中查找用户并返回用户对象，以便 Flask-Login 进行后续的操作。 2. `login_manager.login_view = 'auth.login'`
# 这行代码设置了登录页面的视图函数的名称。在这个例子中，设置了登录页面的视图函数为 `auth.login`，这表示用户在未登录时访问需要登录才能访问的页面时将被重定向到 `auth.login`。 3.
# `login_manager.login_message_category = 'warning'`
# 这行代码设置了登录消息的类别，以便在页面上显示不同类型的消息。在这个例子中，将登录消息的类别设置为警告消息，这样在页面上展示登录相关的消息时将以警告样式显示。 综合起来，这段代码的作用是通过 Flask-Login
# 来设置用户加载函数、设置登录页面的视图函数，并定义了登录消息的类别，以确保用户认证和登录的顺利进行。
