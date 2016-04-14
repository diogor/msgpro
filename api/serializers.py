from rest_framework import serializers

from .models import Mensagem, Identidade


class MensagemSerializer(serializers.HyperlinkedModelSerializer):
    sender_url = serializers.HyperlinkedRelatedField(
        view_name='api:identidade-detail',
        lookup_field='nome',
        source='remetente',
        read_only=True
    )
    sender = serializers.SlugField(source='remetente')
    recipient = serializers.SlugField(source='destinatario')
    date = serializers.DateTimeField(source='data', read_only=True)
    text = serializers.CharField(source='texto')
    class Meta:
        model = Mensagem
        fields = ('sender_url', 'sender', 'recipient', 'date', 'text')


class IdentidadeSerializer(serializers.ModelSerializer):
    name = serializers.SlugField(source='nome')
    class Meta:
        model = Identidade
        fields = ('name', 'pubkey')
