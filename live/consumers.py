import json
from random import randint
from time import time
from django.core import serializers
from channels import Group
from channels.sessions import channel_session

from api.models import Identidade, Mensagem



@channel_session
def ws_connect(message):
    room = "{}.{}".format(str(time()), str(randint(100000, 999999)))
    message.channel_session['room'] = room
    Group("%s" % room).add(message.reply_channel)

    msg = json.dumps({"type": "srv", "text": "Welcome!", "code": 1})
    Group("%s" % room).send({"text": msg})


@channel_session
def ws_message(message):
    room = message.channel_session['room']
    mensagem = json.loads(message.get('text'))
    tipo = mensagem.get('type')

    if tipo == 'id':
        nome = mensagem.get('name')
        pubkey = mensagem.get('pubkey')
        ident, criado = Identidade.objects.get_or_create(nome=nome, pubkey=pubkey)
        ident.online = True
        ident.save()
        message.channel_session['ident'] = ident
        if criado:
            msg = {"type": "nu", "name": nome}
        else:
            msg = {"type": "eu", "name": nome}

        Group("%s" % room).send({"text": json.dumps(msg)})

    if tipo == 'msg':
        destinatario = mensagem.get('recipient')
        remetente = message.channel_session.get('ident')
        text = mensagem.get('text')
        if remetente:
            nova = Mensagem.objects.create(remetente=remetente.nome, destinatario=destinatario, texto=text)

            id_remetente = Identidade.objects.get(nome=destinatario)

            if id_remetente.is_online():
                canal_dest = id_remetente.canal
                msg = serializers.serialize('json', nova)
                Group(canal_dest).send({"text": msg})
            else:
                msg = {"type": 'str', "recipient": id_remetente.nome, "text": nova.texto}
                Group(room).send({"text": json.dumps(msg)})


@channel_session
def ws_disconnect(message):
    ident = message.channel_session.get('ident')
    if ident:
        ident.online = False
        ident.save()
    try:
        Group("%s" % message.channel_session['room']).discard(message.reply_channel)
    except KeyError:
        pass
