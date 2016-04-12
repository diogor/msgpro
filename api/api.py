from datetime import datetime

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from .models import Mensagem, Identidade


class MensagemResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'sender': 'remetente.nome',
        'receipt': 'destinatario.nome',
        'date': 'data',
        'text': 'texto'
    })

    def list(self):
        return Mensagem.objects.all()

    def detail(self, pk):
        return Mensagem.objects.get(id=pk)

    def create(self):
        return Mensagem.objects.create(
            remetente=Identidade.objects.get(nome=self.data['sender']),
            destinatario=Identidade.objects.get(nome=self.data['receipt']),
            texto=self.data['text'],
            data=datetime.now()
        )

    def delete(self, pk):
        Mensagem.objects.get(id=pk).delete()

    def is_authenticated(self):
        # Open everything wide!
        # DANGEROUS, DO NOT DO IN PRODUCTION.
        return True

        # Alternatively, if the user is logged into the site...
        # return self.request.user.is_authenticated()

        # Alternatively, you could check an API key. (Need a model for this...)
        # from myapp.models import ApiKey
        # try:
        #     key = ApiKey.objects.get(key=self.request.GET.get('api_key'))
        #     return True
        # except ApiKey.DoesNotExist:
        #     return False


class IdentidadeResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'name': 'nome',
        'pubkey': 'pubkey'
    })

    def list(self):
        return Identidade.objects.all()

    def detail(self, nome):
        return Identidade.objects.get(nome__exact=nome)

    def create(self):
        return Identidade.objects.create(
            nome=self.data['name'],
            pubkey=self.data['pubkey']
        )

    def is_authenticated(self):
        # Open everything wide!
        # DANGEROUS, DO NOT DO IN PRODUCTION.
        return True

        # Alternatively, if the user is logged into the site...
        # return self.request.user.is_authenticated()

        # Alternatively, you could check an API key. (Need a model for this...)
        # from myapp.models import ApiKey
        # try:
        #     key = ApiKey.objects.get(key=self.request.GET.get('api_key'))
        #     return True
        # except ApiKey.DoesNotExist:
        #     return False
