from rest_framework import viewsets

from .serializers import MensagemSerializer
from .models import Mensagem


class MensagemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Mensagem.objects.all().order_by('-data')
    serializer_class = MensagemSerializer
