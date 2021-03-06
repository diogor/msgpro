from __future__ import unicode_literals

from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models


def upload_to(instance, filename):
    return 'veri/%s/%s' % (instance.nome, filename)


class Identidade(models.Model):
    nome = models.SlugField(unique=True)
    description = models.TextField()
    pubkey = models.TextField()
    shared = models.BooleanField(default=False, editable=False)
    online = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    compromised = models.BooleanField(default=False)
    imagem = models.ImageField(blank=True, upload_to=upload_to)

    def __str__(self):
        return self.nome

    def is_online(self):
        return self.online


class Mensagem(models.Model):
    remetente = models.ForeignKey(Identidade, related_name="caixa_de_saida", on_delete=models.CASCADE)
    destinatarios = models.ManyToManyField(Identidade, related_name="caixa_de_entrada")
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    validade = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('-data',)

    def __str__(self):
        return self.texto

    def is_expired(self):
        return timezone.now() > self.validade


@receiver(pre_save, sender=Mensagem)
def set_expiracao(sender, instance, **kwargs):
    instance.validade = timezone.now() + timedelta(days=settings.VALIDADE_MENSAGEM)
