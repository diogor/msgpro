from rest_framework import viewsets, mixins, filters, generics
from rest_framework.decorators import list_route

from .serializers import MensagemSerializer, IdentidadeSerializer, IdentidadeCreateSerializer
from .models import Mensagem, Identidade


class MultiSerializerViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializers = { 
        'default': None,
    }

    def get_serializer_class(self):
            return self.serializers.get(self.action,
                        self.serializers['default'])

class MensagemViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer


class IdentidadeViewSet(MultiSerializerViewSet):
    """
    API endpoint that allows identities to be viewed or edited.
    """
    lookup_field = 'nome'
    queryset = Identidade.objects.all()
    
    serializers = {
        'list': IdentidadeSerializer,
        'create': IdentidadeCreateSerializer,
        'default': IdentidadeSerializer,
    }
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class IdentidadeSearch(generics.ListAPIView):
    serializer_class = IdentidadeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the messages for
        the identity as determined by the nome portion of the URL.
        """
        nome = self.kwargs.get('q')
        return Identidade.objects.filter(nome__icontains=nome)


class MensagemList(generics.ListAPIView):
    serializer_class = MensagemSerializer

    def get_queryset(self):
        """
        This view should return a list of all the messages for
        the identity as determined by the nome portion of the URL.
        """
        nome = self.kwargs.get('nome')
        return Mensagem.objects.filter(destinatarios__nome=nome)
