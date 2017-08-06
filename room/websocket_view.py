from django.http import HttpResponse
from rest_framework import status

from channels.handler import AsgiHandler
from channels import Group
import json

def pk_from_url(url: str):
    if url[-1] == '/':
        pk = url.split('/')[-2]
    else:
        pk = url.split('/')[-1]
    return pk


def connect_room(message):
    url: str = message.content['path']
    pk = pk_from_url(url)
    message.reply_channel.send({"accept": True})
    Group('room{0}'.format(pk)).add(message.reply_channel)


def disconnect_room(message):
    url: str = message.content['path']
    pk = pk_from_url(url)
    Group('room{0}'.format(pk)).discard(message.reply_channel)


def send_room(message):
    print(message.content)
    body = json.loads(message.content['text'])
    print(body)
    url: str = message.content['path']
    pk = pk_from_url(url)
    # options = body['options']
    # type_operation = body['type']
    Group('room{0}'.format(pk)).send({'text' : json.dumps(body)})
    # try:
    #     draft = SimpleDocumentTemplateDraftHtml.objects.get(pk=pk)
    #     if type_operation == 'add':
    #         draft.add_options(json.loads(options))
    #     elif type_operation == 'remove':
    #         draft.remove_options(json.loads(options))
    #     else:
    #         terminal.print_error('ERROR TYPE OPERATION: {}'.format(type_operation))
    #         pass
    # except SimpleDocumentTemplateDraftHtml.DoesNotExist:
    #     return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    # Group('draft{0}'.format(pk)).send(body)