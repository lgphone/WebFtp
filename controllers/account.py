import tornado
from tornado.web import RequestHandler
from models.webftp_orm import User
import json

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username", None)

class LoginHandler(BaseHandler):
    def get(self):
        self.render('account/login.html')

    def post(self):
        ret = {'status': 'true', 'message': ''}
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        # print(username, password)
        obj = User().select().where(User.username == username, User.password == password).first()
        if obj:
            self.set_secure_cookie("username", username)
        else:
            ret['status'] = 'false'
            ret['message'] = '用户名或密码错误'
        return self.write(json.dumps(ret))


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect("/login")