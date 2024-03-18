# 设置工厂函数
from flask import Flask, render_template, request
from sqlalchemy import inspect

from blueprints.admin import admin as ad_bp
from blueprints.auth import auth as au_bp
from blueprints.blog import blog as bl_bp
from commons.configs import config
import click
import os
import logging
from commons.exts import bootstrap, db, mail, moment, ckeditor, migrate, login_manager, csrf
from commons.models import Admin, Category
from flask_wtf.csrf import CSRFError
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_sqlalchemy.record_queries import get_recorded_queries

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__, template_folder='templates')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_logging(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)

    return app


"""
-  `register_logging(app)`  注册日志功能，用于记录应用程序的运行日志。
-  `register_extensions(app)`  注册扩展，将应用程序所需的扩展添加到应用程序中。
-  `register_blueprints(app)`  注册蓝图，将应用程序的蓝图添加到应用程序中，用于组织和管理不同的功能模块。
-  `register_commands(app)`  注册命令，将应用程序的自定义命令添加到应用程序中，用于执行特定的操作。
-  `register_errors(app)`  注册错误处理，定义应用程序的错误处理函数，用于处理应用程序中可能发生的错误。
-  `register_shell_context(app)`  注册shell上下文，定义应用程序的shell上下文，用于在shell环境中执行特定操作。
-  `register_template_context(app)`  注册模板上下文，定义应用程序的模板上下文，用于在模板中使用特定的变量和函数。
-  `register_request_handlers(app)`  注册请求处理程序，定义应用程序的请求处理函数，用于处理不同类型的请求。"""


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'MyBLOG/BLOG2.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='MyBLOG Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


# 1.定义了一个名为 `RequestFormatter` 的类，它继承自 `logging.Formatter`。这个类的目的是自定义日志记录的格式。在这里，我们想要记录请求的详细信息，包括请求的URL和远程地址。
# 2. 在 `RequestFormatter` 类中，我们重写了 `format` 方法。这个方法接收一个 `record` 参数，它是一个日志记录对象。我们在这里添加了两个属性到 `record` 对象中：`url` 和remote_addr`。这些属性分别表示请求的URL和远程地址。
# 3. 创建了一个 `request_formatter`实例，使用我们自定义的格式字符串。这个格式字符串包含了时间戳、远程地址、URL、日志级别和消息。
# 4. 定义了另一个普通的日志格式化器 `formatter`，它只包含时间戳、日志名称、日志级别和消息。
# 5. 创建了一个 `file_handler`，它是一个 `RotatingFileHandler` 对象。这个处理程序用于将日志写入文件。我们指定了日志文件的路径（`os.path.join(basedir,
# 'BLOG2/BLOG2.log')`），并设置了文件的最大大小（`maxBytes=10 * 1024 *1024`）和备份数量（`backupCount=10`）。这意味着当日志文件达到10MB时，它会被切割，并保留10个备份文件。
# 6. 创建了一个 `mail_handler`，它是一个 `SMTPHandler` 对象。这个处理程序用于通过电子邮件发送错误日志。我们指定了邮件服务器的地址、发件人地址、收件人地址、邮件主题和凭据。它只会处理错误级别的日志。
# 7. 最后的条件语句检查应用是否处于调试模式。如果不是调试模式，将邮件处理程序和文件处理程序添加到应用的日志处理程序中。
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(ad_bp)
    app.register_blueprint(au_bp)
    app.register_blueprint(bl_bp)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        #  这行代码获取了数据库中第一个管理员对象并将其赋值给变量admin。
        # 1. 查询数据库中的所有管理员对象。
        # 2. 获取第一个管理员对象。
        # 3. 将该管理员对象赋值给变量admin。
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):  # 创建虚假数据
    @app.cli.command()
    @click.option('--category', default=10, help='Quality of category, default is 10.')
    @click.option('--post', default=50, help='Quality of posts, default is 50.')
    @click.option('--comment', default=500, help='Quality of comments, default is 500.')
    def forge(category, post, comment):
        from commons.fakes import fake_comments, fake_posts, fake_categories

        db.drop_all()
        db.create_all()

        click.echo('Generating %d categories' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments' % comment)
        fake_comments(comment)

        click.echo('Done.')


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_recorded_queries():
            if q.duration >= app.config['BLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response


# 这段代码的作用是通过注册 @app.after_request 装饰器，实现在每次请求结束后检查数据库查询的性能，并记录慢查询。具体作用如下： 监控数据库查询性能：在每次请求结束后，会调用 query_profiler
# 函数对数据库查询进行性能分析。这可以帮助开发人员监控数据库查询的执行时间，以便发现潜在的性能瓶颈和优化空间。 记录慢查询：通过遍历已记录的查询（使用 get_recorded_queries()
# 函数获取），检查每个查询的执行时间是否超过了预设的阈值 app.config['BLOG_SLOW_QUERY_THRESHOLD']，如果超过阈值则会将该慢查询记录在日志中。
# 日志输出：对于执行时间超过阈值的慢查询，会通过应用程序的日志系统记录警告信息，包括慢查询的执行时间、上下文、执行语句等详细信息


"""
初始化数据库 、 数据库迁移 、数据库更新
flask db init
flask db migrate
flask db upgrade"""


# 使用docker 最初时创建数据库
def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('admin'):
            from commons.models import Admin, Category
            db.create_all()
            admin = Admin(
                username='admin',
                blog_title='My blog',
                blog_sub_title="Welcome to the blog.",
                name='carry',
                info="I'm Carrt. Please write down what you want to write"
            )
            admin.set_password('HelloFlask')
            db.session.add(admin)
            db.session.commit()


if __name__ == '__main__':
    app = create_app('development')
    init_db()
    app.run(debug=True, port=5000)  # 监听所有消息  host='0,0,0,0'
