from .account_url import urlpatterns as account_urls
from .computer_url import urlpatterns as computer_urls
from .queue_url import urlpatterns as queue_urls
from .session_url import urlpatterns as session_urls

urlpatterns = [] + account_urls + computer_urls + queue_urls + session_urls
