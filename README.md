### websocket server
基于[django-private-chat](https://github.com/Bearle/django-private-chat) 和 djangorestframework 的websockt 服务端示例

### 初始化项目

- 创建python虚拟环境
```angular2html
mkvirtualenv -p /usr/bin/python3 websocketserver
```

```
source ~/.virtualenvs/websocketserver/bin/activate
```

- 安装依赖
```
pip install -r requirements.txt
```

- 在WebSocketServer目录下创建`private_config.py `，此文件用于存储云片apikey, 添加`YUNPIAN_APIKEY = ''`
```
cd websocket_server
vim WebSocketServer/private_config.py
```

- 生成数据库
```
# 1. 创建更改的文件
python manage.py makemigrations
# 2. 将生成的py文件应用到数据库
python manage.py migrate
```

- 创建管理员
```
python manage.py createsuperuser
```

- 运行项目
```
python manage.py runserver 8000
```

- 非DEBUG时，需要收集静态文件
```
python manage.py collectstatic --noinput
```

- 运行`run_chat_server`启动websocket 服务
```
python manage.py run_chat_server
```

或者

- 通过`systemd`服务的配置`run_chat_server`
将项目中`bin/chatserver.service`拷贝到`/lib/systemd/system`目录下（注意：修改`.service`中的路径）。

启动websocket 服务
```
sudo systemctl start chatserver.service
```

