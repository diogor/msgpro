from rest_framework import serializers

from .models import Mensagem, Identidade


class MensagemSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.HyperlinkedRelatedField(source='remetente')
    receipt = serializers.HyperlinkedRelatedField(source='destinatario')
    text = serializers.TextField(source='texto')
    date = serializers.DateTimeField(source='data')

    class Meta:
        model = Mensagem
