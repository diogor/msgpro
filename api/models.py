from __future__ import unicode_literals

from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models


class Identidade(models.Model):
    nome = models.SlugField(unique=True)
    pubkey = models.TextField()
    canal = models.CharField(max_length=20, unique=True)
    online = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nome

    def is_online(self):
        return self.online


class Mensagem(models.Model):
    remetente = models.ForeignKey(Identidade, related_name="caixa_de_saida")
    destinatario = models.ForeignKey(Identidade, related_name="caixa_de_entrada")
    tipo = models.CharField(max_length=3, default='msg')
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    validade = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('-data',)

    def __unicode__(self):
        return self.texto

    def is_expired(self):
        return timezone.now() > self.validade


@receiver(pre_save, sender=Mensagem)
def set_expiracao(sender, instance, **kwargs):
    instance.validade = timezone.now() + timedelta(days=settings.VALIDADE_MENSAGEM)
