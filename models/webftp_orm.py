from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
import os
import time
from config import BASE_DIR
db = SqliteExtDatabase(os.path.join(BASE_DIR, 'webftp.db'))
#db = SqliteExtDatabase('/workstation/WebFtp/webftp.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)


class Files(BaseModel):
    file_name = CharField()
    md5 = CharField()
    path = CharField()
    size = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)



def create_tables():
    db.connect()
    db.create_tables([User, Files])
    db.close()
def drop_tables():
    db.connect()
    db.drop_tables([User, Files])
    db.close()

#drop_tables()
#time.sleep(1)
#create_tables()


def save_test():
    user = User()
    user.username = 'shenyang'
    user.password = '123'
    user.save()

def select_test():
    ret = User().select().where(User.username == 'sdf').first()
    # or
    # User.select().where((User.username == 'shenyang') | (User.username == 'wang')).first()
    # and
    # User.select().where((User.username == 'shenyang'), (User.password == '123')).first()
    if ret:
        print(ret.username)
    else:
        print('none have')

def select_all():
    ret = User.select()
    for obj in ret:
        print(obj.username)


def delete_test():
    User.delete().where(User.username == 'shenyang').execute()

def update_test():
    query = User.update(password='wanglu').where(User.username == 'shenyang')
    query.execute()

