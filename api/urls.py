from django.conf.urls import url, include

from .api import MensagemResource, IdentidadeResource

urlpatterns = [
    url(r'^msgs/', MensagemResource.as_list(), name='listar-mensagens'),
    url(r'^msgs/(?P<pk>\d+)/$', MensagemResource.as_detail(), name='mensagem-id'),

    url(r'^idents/', IdentidadeResource.as_list(), name='listar-identidades'),
    url(r'^idents/(?P<nome>[\w-]+)/$', IdentidadeResource.as_detail(), name='identidade-nome'),
]
