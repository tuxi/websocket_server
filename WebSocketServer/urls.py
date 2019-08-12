"""websocket_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve

# django rest_framework
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from WebSocketServer.settings import MEDIA_ROOT, STATICFILES_DIRS, DEBUG

import xadmin

from users.views import SmsCodeViewSet, UserViewSet
from pinax.likes.apiviews import LikeToggleView
from django_private_chat.views.apiview import DialogListViewSet, MessageListViewSet
from home.views import HomeView

# 通过router绑定url
router = DefaultRouter()

# 验证码
router.register(r'code', SmsCodeViewSet, base_name='code')
# 用户
router.register(r'users', UserViewSet, base_name='users')
router.register(r'dialog', DialogListViewSet, base_name='dialog')
# "http://127.0.0.1:8000/api/message/?dialog=1&page=2"
router.register(r'message', MessageListViewSet, base_name='message')

# 用户点赞列表、添加点赞、删除点赞 6
# select *from django_content_type
router.register(r'likes', LikeToggleView, base_name='likes')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api/', include(router.urls)),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATICFILES_DIRS[0]}, name='static'),

    # jwt的认证方式， 在iOS端使用的是jwt的认证方式，未使用rf自带的认证方式
    url(r'^api/login/', obtain_jwt_token),
    # 接受心跳包，验证jwt token是否有效，如果无效则以退出登陆
    url(r'^api/heartbeat/', verify_jwt_token),
    # drf 文档
    url(r'api/docs/', include_docs_urls(title="websocket api docs")),

    # 测试聊天的页面
    # 所有用户页面
    url(r'test/', include('django_private_chat.urls')),
    # 通过username 与某个用户发起对话的页面
    url(r'test/', include('chat.urls')),
    url(r'^$', view=HomeView.as_view(), name='home'),

    # drf自带的认证方式
    # drf登陆的路由为auth/drf/login/ 退出为auth/drf/logout/
    url(r'^auth/drf/', include('rest_framework.urls', namespace='rest_framework')),
]


if DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
