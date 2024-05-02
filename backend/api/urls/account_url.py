from django.urls import path
from rest_framework.routers import DefaultRouter
from ..views import AccountRegister, AccountViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='Account')

# urlpatterns = [
#     path('accounts/register/', AccountRegister.as_view(), name='Account Register'),
# ]

# urlpatterns += router.urls
urlpatterns = [] + router.urls