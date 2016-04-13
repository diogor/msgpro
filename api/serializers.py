from rest_framework import serializers

from .models import Mensagem, Identidade


class MensagemSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.CharField(source='remetente.nome')
    receipt = serializers.CharField(source='destinatario.nome')
    text = serializers.CharField(source='texto')
    date = serializers.DateTimeField(source='data')

    class Meta:
        model = Mensagem
