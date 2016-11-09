# -*- coding: utf-8 -*-
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
        try:
            ident = Identidade.objects.get(nome=nome)
        except Identidade.DoesNotExist:
            ident = False

        if not ident:
            ident = Identidade.objects.create(nome=nome, pubkey=pubkey, canal=room)
            msg = {"type": "usr", "name": nome, "code": 0, "text": "Identidade criada."}
        else:
            msg = {"type": "usr", "name": nome, "code": 1, "text": "Identidade existente."}

        message.channel_session['ident'] = ident.id
        ident.online = True
        ident.save()
        Group("%s" % room).send({"text": json.dumps(msg)})

    if tipo == 'msg':
        destinatario = mensagem.get('recipient')
        remetente_id = message.channel_session.get('ident')
        remetente = Identidade.objects.get(id=remetente_id)

        try:
            id_destinatario = Identidade.objects.get(nome=destinatario)
        except Identidade.DoesNotExist:
            msg = {"type": "usr", "name": destinatario, "code": 2, "text": "O usuário não existe."}
            Group(room).send({"text": json.dumps(msg)})

        text = mensagem.get('text')
        if remetente:
            nova = Mensagem.objects.create(remetente=remetente, destinatario=id_destinatario, texto=text)
            if id_destinatario.is_online():
                canal_dest = id_destinatario.canal
                msg = {"type": 'msg', "sender": nova.remetente.nome, "text": nova.texto, "date": nova.data}
                Group(canal_dest).send({"text": json.dumps(msg)})
            else:
                msg = {"type": 'str', "recipient": id_destinatario.nome, "text": nova.texto}
                Group(room).send({"text": json.dumps(msg)})


@channel_session
def ws_disconnect(message):
    ident_id = message.channel_session.get('ident')
    ident = Identidade.objects.get(id=ident_id)
    if ident:
        ident.online = False
        ident.save()
    try:
        Group("%s" % message.channel_session['room']).discard(message.reply_channel)
    except KeyError:
        pass
