from django.utils.dateformat import format as dateformat
from rest_framework import serializers

from .models import Mensagem, Identidade


class MensagemSerializer(serializers.HyperlinkedModelSerializer):
    sender_url = serializers.HyperlinkedRelatedField(
        view_name='api:identidade-detail',
        lookup_field='nome',
        source='remetente',
        read_only=True
    )
    sender = serializers.SlugRelatedField(
        source='remetente',
        many=False,
        read_only=False,
        queryset=Identidade.objects.all(),
        slug_field='nome'
     )
    recipients = serializers.SlugRelatedField(
        source='destinatarios',
        many=True,
        read_only=False,
        queryset=Identidade.objects.all(),
        slug_field='nome'
     )
    date = serializers.SerializerMethodField()
    text = serializers.CharField(source='texto')

    def get_date(self, obj):
        return dateformat(obj.data, 'U')

    class Meta:
        model = Mensagem
        fields = ('id', 'sender_url', 'sender', 'recipients', 'date', 'text')


class IdentidadeSerializer(serializers.ModelSerializer):
    name = serializers.SlugField(source='nome')
    class Meta:
        model = Identidade
        fields = ('name', 'pubkey', 'description', 'verified', 'compromised', 'shared')

class IdentidadeCreateSerializer(serializers.ModelSerializer):
    name = serializers.SlugField(source='nome')
    image = serializers.ImageField(source='imagem', use_url=False, required=False)
    class Meta:
        model = Identidade
        fields = ('name', 'pubkey', 'description', 'image', 'shared')

