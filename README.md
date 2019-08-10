### websocket server
基于[django-private-chat](https://github.com/Bearle/django-private-chat) 和 djangorestframework 的websockt 服务端示例


### 前端示例
http://chat.enba.com/dialogs/
需要先登录
```
useername: xiaoyuan
password: admin123

useername: user1
password: admin123
```

### 初始化项目

- python3.6

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

### 运行前端示例

- 请先配置客户端请求的host和port
```
CHAT_WS_CLIENT_HOST = '127.0.0.1'
CHAT_WS_CLIENT_PORT = 80
CHAT_WS_CLIENT_ROUTE = 'ws/'
```

- 运行
```
python manage.py runserver 8000
```

- 非DEBUG时，需要收集静态文件
```
python manage.py collectstatic --noinput
```

### 运行websocket服务端

- 请先配置websocket监听的host和port
```
CHAT_WS_SERVER_PROTOCOL = 'ws'
CHAT_WS_SERVER_HOST = '127.0.0.1'
CHAT_WS_SERVER_PORT = 5002
```

- 运行`run_chat_server`启动websocket 服务
```
python manage.py run_chat_server
```

或者

- 通过`systemd`服务的配置`run_chat_server`
将项目中`bin/chatserver.service`拷贝到`/lib/systemd/system`目录下（注意：修改`.service`中的项目路径）。
```
cp bin/chatserver.service /lib/systemd/system
```

启动websocket 服务
```
sudo systemctl start chatserver.service
```

如果时修改或新建的服务文件需要先执行`systemctl daemon-reload` ，告诉systemd系统，然后再启动`chatserver.service`，不然无法正常启动。

### 问题

- 问题1: 本地测试环境下websocket正常工作，但是本地服务器使用nginx反向代理未正常在线，显示`WebSocket is already in CLOSING or CLOSED state.`。

解决：
此问题是由webSocket在nginx的proxy_pass配置错误导致的，`proxy_pass http://websocket_server;`修改为`proxy_pass http://websocket_server/;`问题解决。

- 问题2: 生产环境部署到阿里云ECS时，使用nginx做websocket的反向代理后，客户端请求总是502。
同样的配置，在本地服务器通过nginx没有，但是阿里云ECS部署就会导致502错误。
Error：`enba:186 WebSocket connection to 'ws://chat.enba.com/ws/9ygfrczj6le3buh28b393cv20w5hzj4l/enba' failed: Error during WebSocket handshake: Unexpected response code: 502`

解决：
由于websocket服务使用`python manage.py run_chat_server`命令开启的，并且绑定的`host`为`localhost`、port为`5002`，通过`netstat -atnp`命令在本地服务器查询到`5002`网络端口已开启，而在阿里云ECS服务端未查询到此网络端口，期间很是郁闷，不过此时我已经找到了问题所在。此问题是由于nginx配置错误导致，在nginx的proxy_pass为`127.0.0.1:5002`，而websockets监听的为`localhost：5002`，导致反向代理失败。通过修改初始化`websockets.serve()`方法的`host`参数将`localhost`修改为`127.0.0.1`问题解决，重启`chatserver.service`问题解决。