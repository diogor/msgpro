from django.conf.urls import url, include
from rest_framework import routers

from .views import MensagemViewSet


router = routers.DefaultRouter()
router.register(r'msgs', MensagemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
