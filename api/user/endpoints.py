from django.urls import path, include
from rest_framework import routers
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from . import api
router = routers.DefaultRouter()
router.register('users',api.UserModelViewSet)
router.register('fcm-devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path('', include(router.urls)),

]