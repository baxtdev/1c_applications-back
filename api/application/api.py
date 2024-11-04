from rest_framework import viewsets,permissions

from api.mixins import UltraSupperViewSet

from .serializers import Application,ApplicationSerializer,ApplicationTotalAmount,ApplicationTotalAmountSerializer,\
    ApplicationPayment,ApplicationPaymentSerializer,ApplicationReconciliators,ApplicationReconciliatorsSerializer




class ApplicationViewSet(UltraSupperViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    serializer_classes = {
        'list': ApplicationSerializer,
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
    }

