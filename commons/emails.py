from flask import url_for, current_app
from flask_mail import Message
from commons.exts import mail
from threading import Thread


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html, sync=False):
    message = Message(subject=subject, recipients=[to], html=html)
    if sync:
        mail.send(message)
    else:
        Thread(target=_send_async_mail,
               args=(current_app._get_current_object(), message)).start()
# 这段代码用于发送电子邮件，支持同步和异步发送。具体功能如下：
# 1.  `send_email` 函数用于发送电子邮件，接收主题、发件人、收件人、文本正文、HTML正文、附件等参数。
# 2. 创建一个 `Message` 对象，设置邮件的相关信息。
# 3. 如果有附件，将附件添加到邮件中。
# 4. 根据 `sync` 参数判断是否需要同步发送邮件：
#    - 如果 `sync` 为 `True` ，则直接调用 `mail.send(msg)` 同步发送邮件。
#    - 如果 `sync` 为 `False` ，则创建一个新线程，调用 `send_async_email` 函数来异步发送邮件。
# 5.  `send_async_email` 函数在应用上下文中发送邮件，确保能够访问Flask应用的上下文信息。
# 这段代码的设计考虑到了同步和异步发送邮件的需求，并且在异步发送邮件时使用了线程来提高性能


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='New comment', to=current_app.config['MAIL_USERNAME'],
              html='<p>New comment in post <i>%s</i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></P>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='New reply', to=comment.email,
              html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (comment.post.title, post_url, post_url))
