from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models

class Identidade(models.Model):
    nome = models.SlugField(unique=True)
    pubkey = models.TextField()

    def __unicode__(self):
        return self.nome


class Mensagem(models.Model):
    remetente = models.ForeignKey(Identidade, related_name="caixa_de_saida")
    destinatario = models.ForeignKey(Identidade, related_name="caixa_de_entrada")
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    validade = models.IntegerField(default=3)

    def __unicode__(self):
        return self.texto

    def is_expired(self):
        prazo = self.data + timedelta(days=self.prazo)
        return datetime.now() > prazo
