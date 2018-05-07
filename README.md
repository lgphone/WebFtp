# WebFtp
## 基于Tornado + Nginx 设计的上传下载服务器
* 数据库使用 sqlite3 和 peewee ORM
* 前端使用了Bootsrap 框架
* 基于Tornado的secure_cookie 进行用户认证
## 实现功能：
* 用户登录登出
* 登陆后列出已经上传的文件
* 用户上传，下载文件
* 管理员接口，列出已有用户，可以添加删除普通用户
## 路由:
* /login 登录
* /logout 登出
* /index 主页
* /admin 管理员

## 重要提示
admin 页面没有进行权限认证，请在Nginx中配置只允许特定IP地址访问此路由
例如只允许 192.168.1.127：
```
 allow 192.168.1.127;
 deny all;
```

## 需要给Nginx打补丁来支持nginx 文件上传功能
* 下载 https://github.com/Austinb/nginx-upload-module
* 解压后放到和nginx源代码同一目录下
* 编译参数
```
--add-module=../nginx-upload-module
```

## nginx 配置
#### WebFtp.conf
```
upstream tornadoes {
    #server 192.168.1.12:8000;
    server 127.0.0.1:8000;
}


server {
    listen 80;
    server_name up.izhihu.me;
    
    location = / {
      rewrite (.*) /index;
    }   
   
    location = /favicon.ico {
       rewrite (.*) /static/favicon.ico;
    }

    location /static/ {
        root /usr/local/WebFtp;
        if ($query_string) {
            expires max;
        }
    }

    location /upload {
        upload_pass @py;
        upload_cleanup 400 404 499 500-505;
        upload_store /tmp/upload_tmp;
        upload_store_access user:rw;
        upload_limit_rate 0;
        upload_set_form_field "file_name" $upload_file_name;
        upload_set_form_field "content_type" $upload_content_type;
        upload_set_form_field "tmp_path" $upload_tmp_path;
        upload_aggregate_form_field "md5" $upload_file_md5;
        upload_aggregate_form_field "size" $upload_file_size;
        upload_pass_form_field "^.*$";
    }
    
    location @py {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://tornadoes;
    }
   
    location ^~ /download {
        alias /tmp/upload_tmp;
    }
    
    location /admin {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://tornadoes;
        allow 192.168.1.127;
        deny all;
    }

    location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://tornadoes;
    }
    access_log logs/webftp.access.log yang;
}
```
#### 修改Nginx主配置文件，来提高上传文件的大小
```
client_max_body_size        4096M;
```
#### 修改程序的配置下载目录和nginx的上传目录保持一致，并保证此目录用户为 nginx 运行用户
```
config.py
DOWNLOAD_DIR = '/tmp/upload_tmp'
```
注意Nginx配置文件中的static 路径为WebFtp服务器的根目录，用来代理static目录

## 运行
```python3 app.py```
## 运行界面
登录界面
![登录界面](https://github.com/lgphone/WebFtp/blob/master/doc/pic/login.png)
主界面
![主界面](https://github.com/lgphone/WebFtp/blob/master/doc/pic/index.png)
管理员界面
![管理员界面](https://github.com/lgphone/WebFtp/blob/master/doc/pic/admin.png)

## 暂时就这些
下一步会添加进度条显示，也是依赖于nginx的一个补丁实现的
# add test
