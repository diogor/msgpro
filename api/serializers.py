from rest_framework import serializers

from .models import Mensagem, Identidade


class MensagemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mensagem
        fields = ('remetente', 'destinatario', 'data', 'texto')
