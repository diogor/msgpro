from django.conf.urls import url, include
from rest_framework import routers

from .views import MensagemViewSet, IdentidadeViewSet, MensagemList, IdentidadeSearch


router = routers.DefaultRouter()
router.register(r'msgs', MensagemViewSet)
router.register(r'idents', IdentidadeViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^inbox/(?P<nome>[\w-]+)/$', MensagemList.as_view()),
    url(r'^search/ident/(?P<q>[\w-]+)/$', IdentidadeSearch.as_view()),
]
