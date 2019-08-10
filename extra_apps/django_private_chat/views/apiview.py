from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, authentication, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import filters

from django_private_chat.filters import LikeFilter
from django_private_chat.models import Dialog, Message
from utils.utils import CustomPagination
from django_private_chat.serializers import DialogDetailSerializer, DialogCreateSerializer, MessageDetailSerializer, MessageCreateSerializer


class DialogListView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    retrieve:
        根据dialog id获取会话详情
    create:
        创建会话
    list:
        获取当前用户的所有会话列表, 分页，排序
    destory:
        根据id删除会话

    '''
    serializer_class = DialogDetailSerializer
    # 自定义分页
    pagination_class = CustomPagination
    ordering_fields = ('modified', 'created')
    # 单独在此视图中配置访问权限, 必须登录才能访问，如果登录了，将登录的用户和登录的令牌存在request中
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        dialogs = Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
        return dialogs


    def get_permissions(self):
        return [permissions.IsAuthenticated()]


    def get_serializer_class(self):
        if self.action == "retrieve":
            return DialogDetailSerializer
        elif self.action == "create":
            return DialogCreateSerializer

        return DialogDetailSerializer

    def destroy(self, request, *args, **kwargs):
        return super(DialogListView, self).destroy(request)



class MessageListView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    create:
        创建message
    list:
        获取当前用户与某个用户的会话的所有消息
    destory:
        根据id删除message

    '''
    serializer_class = MessageDetailSerializer
    # 自定义分页
    pagination_class = CustomPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 根据回话id获取所有聊天内容
    filter_class = LikeFilter

    # 按照时间排序消息
    ordering_fields = ('created', )
    # 单独在此视图中配置访问权限, 必须登录才能访问，如果登录了，将登录的用户和登录的令牌存在request中
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        messages = Message.objects.all()
        return messages

    def get_permissions(self):
        return [permissions.IsAuthenticated()]


    def get_serializer_class(self):
        if self.action == "create":
            return MessageCreateSerializer

        return MessageDetailSerializer

    def destroy(self, request, *args, **kwargs):
        return super(MessageListView, self).destroy(request)

