from django.db.models import Q

from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from .serializers import ApplicationSerializer,ApplicactionMaterialSerializer

class ApplicationService:
    @action(detail=False, methods=['post'], url_path='change-status')
    def change_status(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            application = serializer.save()
            application_data = ApplicationSerializer(application).data
            return Response({"detail":"Статус успешно изменен",**application_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # if user.is_superuser:
        #     return queryset

        if user.role == 'OBSERVER':
            return queryset.filter(reconciliators__user__in=[self.request.user])
        

        return queryset.filter(
            Q(
                purchase_reconciliations_status="СONFIRMED",
                reconciliators__user=user,
                reconciliators__is_current=True)|
            Q(
                purchase_reconciliations__user=user,
                purchase_reconciliations__is_current=True)
            )  

    @action(detail=False, methods=['post'], url_path='change-purchase-status')
    def change_purchase_status(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            application = serializer.save()
            application_data = ApplicationSerializer(application).data
            return Response({"detail":"Статус закупа успешно изменен",**application_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='cancel-material-for-purchase')
    def cancel_material_for_purchase(self,request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            application = serializer.save()
            application_data = ApplicactionMaterialSerializer(application).data
            return Response({"detail":"Статус материала успешно отменон",**application_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
