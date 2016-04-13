from rest_framework import serializers

from .models import Mensagem, Identidade


class MensagemSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.SlugField(source='remetente')
    receipt = serializers.SlugField(source='destinatario')
    date = serializers.DateTimeField(source='data', read_only=True)
    text = serializers.CharField(source='texto')
    class Meta:
        model = Mensagem
        fields = ('sender', 'receipt', 'date', 'text')
