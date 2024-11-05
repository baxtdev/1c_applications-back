from rest_framework import viewsets,permissions

from api.mixins import UltraSupperViewSet,MultipleDestroyMixinSerializer

from .serializers import Application,ApplicationSerializer,ApplicationCreateSerializer,ApplicationTotalAmount,ApplicationTotalAmountSerializer,\
    ApplicationPayment,ApplicationPaymentSerializer,ApplicationReconciliators,ApplicationReconciliatorsSerializer




class ApplicationViewSet(UltraSupperViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    serializer_classes = {
        'list': ApplicationSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer,
        'multiple_create':ApplicationCreateSerializer,
        'multiple_update':ApplicationCreateSerializer
    }
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status','importance','contract_number']   
    ordering_fields = ['created_at', 'created_date']
    search_fields = ['id', 'initiator', 'contract_number', 'supplier',]
    permission_classes_by_action = {
        'list': [permissions.IsAdminUser],
        'create': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }


class ApplicationTotalAmountViewSet(UltraSupperViewSet):
    queryset = ApplicationTotalAmount.objects.all()
    serializer_class = ApplicationTotalAmountSerializer 
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['application']
    ordering_fields = ['total_amount']
    search_fields = ['id', 'total_amount']
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated],
        'create': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAdminUser],
    }
    serializer_classes = {
        'list': ApplicationTotalAmountSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer
    }



class ApplicationPaymentViewSet(UltraSupperViewSet):
    queryset = ApplicationPayment.objects.all()
    serializer_class = ApplicationPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['application']
    ordering_fields = ['payment_date', 'payment_amount']
    search_fields = ['id', 'payment_date', 'payment_amount']
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated],
        'create': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAdminUser],
        
    }
    serializer_classes  = {
        'list': ApplicationPaymentSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer
    }


class ApplicationReconciliatorsViewSet(UltraSupperViewSet):
    queryset = ApplicationReconciliators.objects.all()
    serializer_class = ApplicationReconciliatorsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['application','user','user__role','role']
    ordering_fields = ['id']
    search_fields = ['id']
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated],
        'create': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAdminUser],
    }
    serializer_classes  = {
        'list': ApplicationReconciliatorsSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer
    }

