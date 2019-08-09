import xadmin
from .models import Dialog, Message


class DialogAdmin(object):
    list_display = ('id', 'created', 'modified', 'owner', 'opponent')
    list_filter = ('created', 'modified', 'owner', 'opponent')


xadmin.site.register(Dialog, DialogAdmin)


class MessageAdmin(object):
    list_display = (
        'id',
        'created',
        'modified',
        'is_removed',
        'dialog',
        'sender',
        'text',
    )
    list_filter = ('created', 'modified', 'is_removed', 'dialog', 'sender')


xadmin.site.register(Message, MessageAdmin)
