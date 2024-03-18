from flask import request, redirect, url_for

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin


#
# 详细分析
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
# 1. 引入需要的模块：
#    - 首先是引入了 Flask 框架的一些模块，包括 `request`、`redirect`、`url_for`、`current_app`，这些模块提供了处理请求、重定向和生成 URL 的功能。
#    - 接着使用了 Python 2/3 兼容的方式引入了 `urlparse` 和 `urljoin` 函数，用于处理 URL 相关的操作。
# 2. `is_safe_url(target)` 函数：
#    - 这个函数用于判断目标 URL 是否为安全的，其主要逻辑是：
#      - 提取当前请求的 host URL 和目标 URL 的信息，包括 scheme（HTTP/HTTPS）和 netloc（域名和端口）。
#      - 判断目标 URL 的 scheme 是否为 `http` 或 `https`，并且 netloc 是否与请求的 host URL 的 netloc 相同。
#      - 如果上述条件均满足，则认为目标 URL 是安全的，返回 True；否则返回 False。
# 3. `redirect_back(default='blog.index', **kwargs)` 函数：
#    - 这是一个自定义的重定向函数，用于执行安全的页面重定向操作。
#    - 首先尝试从请求参数中获取名为 `next` 的 URL，如果不为空且是安全的，则重定向到该 URL。
#    - 如果不存在或者不安全，则尝试从请求的引用页 `referrer` 中获取 URL，如果不为空且是安全的，则重定向到该 URL。
#    - 如果以上两个途径均不符合要求，将使用 `url_for` 生成一个默认的 URL，然后进行重定向。
# 这段代码主要用于在 Flask 应用中执行安全的重定向操作，确保重定向的目标 URL 是被信任和合法的，以防止恶意重定向等安全问题。
