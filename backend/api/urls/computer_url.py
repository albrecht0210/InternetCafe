from rest_framework.routers import DefaultRouter
from ..views import ComputerViewSet

router = DefaultRouter()
router.register(r'computers', ComputerViewSet, basename='Computer')

urlpatterns = [] + router.urls
