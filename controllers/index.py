import tornado
import tornado.web
import os
import json
from models.webftp_orm import User, Files
from config import DOWNLOAD_DIR
from controllers.account import BaseHandler

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        file_list = []
        objs = Files.select()
        for obj in objs:
            file_list.append([obj.file_name, obj.md5, obj.size, obj.created_date])
        self.render('index/index.html', file_list=file_list, username=self.get_current_user())

class UploadFileNginxHandle(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        ret = {'status': 'true', 'message': '', 'data': ''}
        file_name = self.get_argument("file_name")
        tmp_path = self.get_argument("tmp_path")
        md5 = self.get_argument("md5")
        size = self.get_argument("size")
        if file_name and tmp_path and md5 and size:
            file_path = os.path.join(DOWNLOAD_DIR, file_name)
            os.rename(tmp_path, file_path)
            file_obj = Files()
            file_obj.file_name = file_name
            file_obj.md5 = md5
            file_obj.path = tmp_path
            file_obj.size = size
            file_obj.save()
            ret['data'] = {'name': file_name, 'size': size, 'path': file_path, 'md5': md5}
        ret['status'] = 'false'
        self.write(json.dumps(ret))


class AdminHandle(tornado.web.RequestHandler):
    def get(self):
        user_list = []
        objs = User.select()
        for obj in objs:
            user_list.append([obj.username, obj.password, obj.created_date])
        self.render('index/admin.html', user_list=user_list, username='admin')

    def post(self, *args, **kwargs):
        ret = {'status': 'ture', 'message': '', 'data': ''}
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if username and password:
            user_obj = User()
            user_obj.username = username
            user_obj.password = password
            try:
                user_obj.save()
                ret['message'] = '用户添加成功'
            except Exception as e:
                print(e)
                ret['status'] = 'false'
                ret['message'] = '添加失败，数据库写入失败'
        else:
            ret['status'] = 'false'
            ret['message'] = '用户名或者密码没有填写'
        return self.write(json.dumps(ret))

    def delete(self, *args, **kwargs):
        ret = {'status': 'ture', 'message': '', 'data': ''}
        username = self.get_argument('username', None)
        if username:
            if User.delete().where(User.username == username).execute():
                return self.write(json.dumps(ret))
            else:
                ret['status'] = 'false'
                ret['message'] ='删除失败'
        else:
            ret['status'] = 'false'
            ret['message'] = '没有用户'