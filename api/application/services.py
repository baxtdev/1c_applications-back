from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from .serializers import ApplicationSerializer

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
