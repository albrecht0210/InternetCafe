from rest_framework.routers import DefaultRouter
from ..views import QueueViewSet

router = DefaultRouter()
router.register(r'queues', QueueViewSet, basename='Queue')

urlpatterns = [] + router.urls
