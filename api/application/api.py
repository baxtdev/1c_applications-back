from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes


from api.mixins import UltraSupperViewSet,MultipleDestroyMixinSerializer

from .serializers import Application,ApplicationSerializer,ApplicationCreateSerializer,ApplicationListSerializer,\
    ApplicationTotalAmount,ApplicationTotalAmountSerializer,\
    ApplicationPayment,ApplicationPaymentSerializer,ApplicationCreatePaymentSerializer,\
    ApplicationReconciliators,ApplicationReconciliatorsSerializer,ApplicationReconciliatorsCreateSerializer,\
    ApplicationStatusChange,ApplicationTotalAmountCreateSerializer,ApplicationPurchaseStatusChange,ApplicactionMaterialCancelSerializer\
    
from .services import ApplicationService
from ..permissions import IsMainEmployee



class ApplicationViewSet(ApplicationService,UltraSupperViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    serializer_classes = {
        'list': ApplicationListSerializer,
        'retrieve':ApplicationListSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer,
        'multiple_create':ApplicationCreateSerializer,
        'multiple_update':ApplicationCreateSerializer,
        'change_status':ApplicationStatusChange,
        'change_purchase_status':ApplicationPurchaseStatusChange,
        'cancel_material_for_purchase':ApplicactionMaterialCancelSerializer
    }
    permission_classes = [permissions.IsAuthenticated | IsMainEmployee]
    filterset_fields = ['status','importance','contract_number','reconciliators__status']   
    ordering_fields = ['created_at', 'created_date']
    search_fields = ['id', 'initiator', 'contract_number', 'supplier',]
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated],
        'create': [IsMainEmployee],
        'destroy': [IsMainEmployee],
        'change_status': [permissions.IsAuthenticated],
        'change_purchase_status':[permissions.IsAuthenticated]
    }

class ApplicationTotalAmountViewSet(UltraSupperViewSet):
    queryset = ApplicationTotalAmount.objects.all()
    serializer_class = ApplicationTotalAmountCreateSerializer 
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
        'list': ApplicationTotalAmountCreateSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer
    }



class ApplicationPaymentViewSet(UltraSupperViewSet):
    queryset = ApplicationPayment.objects.all()
    serializer_class = ApplicationCreatePaymentSerializer
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
        'list': ApplicationCreatePaymentSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer
    }


class ApplicationReconciliatorsViewSet(UltraSupperViewSet):
    queryset = ApplicationReconciliators.objects.all()
    serializer_class = ApplicationReconciliatorsCreateSerializer
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
        'list': ApplicationReconciliatorsCreateSerializer,
        'multiple_delete':MultipleDestroyMixinSerializer
    }

