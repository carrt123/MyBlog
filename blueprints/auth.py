# 用户认证
from flask import Blueprint, render_template, flash, redirect, url_for
from commons.forms import LoginForm
from commons.models import Admin
from flask_login import current_user, login_user, logout_user, login_required
from commons.utils import redirect_back

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        flash('Login success', 'success')
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()


@auth.route('/login/flash')
def test_flash():
    flash("这是一条闪现消息", 'info')
    flash("这是一条成功消息", 'success')
    flash("这是一条警告消息", 'warning')
    flash("这是一条测试消息", 'matrix')
    return render_template('base.html')
