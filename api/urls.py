from django.conf.urls import url, include
from rest_framework import routers

from .views import MensagemViewSet, IdentidadeViewSet, IdentidadeCompartilhadaViewSet, MensagemList


router = routers.DefaultRouter()
router.register(r'msgs', MensagemViewSet)
router.register(r'idents', IdentidadeViewSet)
router.register(r'shared-idents', IdentidadeCompartilhadaViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^inbox/(?P<nome>[\w-]+)/$', MensagemList.as_view()),
]
