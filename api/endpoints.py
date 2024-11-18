from rest_framework import routers
from django.urls import include, path

from .yasg import urlpatterns as url_doc
from .auth.endpoints import urlpatterns as auth_urls
from .user.endpoints import urlpatterns as users_urls
from .application.endpoints import urlpatterns as application_urls

urlpatterns=[
    path('',include(users_urls)),
    path('accounts/', include(auth_urls)),
    path('', include(application_urls)), 
]

urlpatterns+=url_doc