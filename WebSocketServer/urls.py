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
from rest_framework_jwt.views import obtain_jwt_token

from WebSocketServer.settings import MEDIA_ROOT, STATICFILES_DIRS, DEBUG

import xadmin

from users.views import SmsCodeViewSet, UserViewSet
from pinax.likes.apiviews import LikeToggleView
from django_private_chat.views.apiview import DialogListViewSet, MessageListViewSet

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
    # drf自带的认证方式
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # jwt的认证方式
    url(r'^login/', obtain_jwt_token),
    # drf 文档
    url(r'docs/', include_docs_urls(title="websocket api docs")),
    # url(r"^likes/", include("pinax.likes.urls", namespace="pinax_likes")),

    url(r'', include('django_private_chat.urls')),
    url(r'', include('chat.urls'))
]


if DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
