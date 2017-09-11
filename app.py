#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
from controllers import index
from controllers import account

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': '43809138f51b96f8ac24e79b3a2cb482',
    'login_url': '/login',
    #'xsrf_cookies': True,
    'debug': True,
    'autoreload': True,
}

application = tornado.web.Application([
    # 主页
    (r"/index", index.IndexHandler),
    # Admin
    (r"/admin", index.AdminHandle),
    # 登录
    (r"/login", account.LoginHandler),
    # 登出
    (r"/logout", account.LogoutHandler),
    # 上传
    (r"/upload", index.UploadFileNginxHandle),
], **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
