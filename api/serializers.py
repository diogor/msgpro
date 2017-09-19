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
    recipient = serializers.SlugRelatedField(
        source='destinatario',
        many=False,
        read_only=False,
        queryset=Identidade.objects.all(),
        slug_field='nome'
     )
    date = serializers.DateTimeField(source='data', read_only=True)
    text = serializers.CharField(source='texto')
    type = serializers.CharField(source='tipo')
    class Meta:
        model = Mensagem
        fields = ('id', 'sender_url', 'sender', 'recipient', 'date', 'type', 'text')


class IdentidadeSerializer(serializers.ModelSerializer):
    name = serializers.SlugField(source='nome')
    class Meta:
        model = Identidade
        fields = ('name', 'pubkey', 'description', 'verified', 'compromised')

class IdentidadeCreateSerializer(serializers.ModelSerializer):
    name = serializers.SlugField(source='nome')
    image = serializers.ImageField(source='imagem', use_url=False)
    class Meta:
        model = Identidade
        fields = ('name', 'pubkey', 'description', 'image')

