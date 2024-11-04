from django.urls import path,include

from rest_framework.routers import DefaultRouter
from . import api

router =  DefaultRouter()
router.register('applications', api.ApplicationViewSet)
router.register('application-payments', api.ApplicationPaymentViewSet)
router.register('application-total-amounts', api.ApplicationTotalAmountViewSet)
router.register('application-reconciliators', api.ApplicationReconciliatorsViewSet)


urlpatterns = [
    path('',include(router.urls))
]

