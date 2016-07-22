import json
from random import randint
from time import time
from channels import Group
from channels.sessions import channel_session

from api.models import Identidade

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    room = "{}.{}".format(str(time()), str(randint(100000, 999999)))
    message.channel_session['room'] = room
    Group("%s" % room).add(message.reply_channel)

    msg = json.dumps({"CH": room})
    Group("%s" % room).send({"text": msg})


@channel_session
def ws_message(message):
    room = message.channel_session['room']
    mensagem = json.loads(message.get('text'))
    print mensagem
    tipo = mensagem.get('type')

    if tipo == 'ident':
        print "d"
        nome = mensagem.get('name')
        pubkey = mensagem.get('pubkey')
        ident, criado = Identidade.objects.get_or_create(nome=nome, pubkey=pubkey)
        if criado:
            msg = {"type": "newuser", "name": nome}
        else:
            msg = {"type": "existinguser", "name": nome}

        Group("%s" % room).send({"text": json.dumps(msg)})


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    try:
        Group("%s" % message.channel_session['room']).discard(message.reply_channel)
    except KeyError:
        pass
