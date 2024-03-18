# 博客前台
from commons.models import Post, Comment, Category
from flask import current_app, render_template, Blueprint, request, url_for, flash, redirect
from commons.forms import AdminCommentForm, CommentForm
from flask_login import current_user
from commons.exts import db
from commons.emails import send_new_comment_email, send_new_reply_email
from commons.utils import redirect_back
from redis_services import like_service
blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # 这段代码用于从请求参数中获取名为page的参数值，如果没有该参数则默认为1，并将其转换为整数类型赋值给变量page。
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    # paginate(page, per_page=per_page): 将结果分页显示，每页显示的数量由per_page指定，显示的页数由page指定。
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog.route('/about')
def about():
    return render_template('blog/about.html')


@blog.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    # 这段代码用于从请求参数中获取名为page的参数值，如果没有该参数则默认为1，并将其转换为整数类型赋值给变量page。
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page=page, per_page=per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:  # send message based on authentication status
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            send_new_comment_email(post)  # send notification email to admin
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


@blog.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) +
                    '#comment-form')


@blog.route('/configs')
def configs_view():
    with current_app.app_context():
        print(current_app.config)
    return 'view configs'


@blog.route('/likes/post', methods=['GET', 'POST'])
def show_like():
    post_id = int(request.args.get('post'))
    print(post_id)
    # 假设在真实场景中，这里会使用 ORM 或 SQL 语句来更新数据库中对应评论的点赞数量
    post_model = Post.query.get(post_id)
    post_model.likes += 1
    db.session.commit()
    return redirect_back()


@blog.route('/query')
def test():
    from sqlalchemy import Select
    model = Select(Category).where(Category.name == "科技科普")
    print(model)
    model = Category.query.filter_by(name="科技科普").first()
    print(model.id)
    return "query!"
