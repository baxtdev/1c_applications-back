from django.db.transaction import atomic
from django.utils.timezone import now


from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer

from rest_framework import status,permissions,viewsets,mixins,filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView



from django_filters.rest_framework import DjangoFilterBackend

from .filters import UserFilterSet

from ..mixins import SuperModelViewSet,IsSuperAdmin,\
    SerializersByAction,PermissionByAction

from .services import ResetPasswordService,UserModelService,PhoneNumberChangeService
from api.user.serializers import (
    GoogleAuthSerializer, 
    RegisterUserSerializer,
    ResetPasswordSerializer,ResetPasword, 
    UserProfileSerializer,User,UserSerializer,
    PhoneNumberChangeSerializer,PhoneNumberChange,
    SetPinCodeSerializer,VerifyPinCodeSerializer,
    )


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_serializer = UserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
        })



class GoogleAuthAPIView(GenericAPIView):
    serializer_class =  GoogleAuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = DefaultUserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })


    
class GetResetPasswordCodeAPIView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserProfileSerializer
    lookup_field = 'phone'

    def get_object(self):
        try:
            return self.queryset.get(phone=self.kwargs['phone'])
        
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден")

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        reset_password_code = ResetPasword.objects.create(user=user, is_active=True)

        return get_ok_response('Вам отправлен код')



class CheckingCodeAPIView(GenericAPIView):
    queryset = ResetPasword.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer
    lookup_field = 'code'

    def get_object(self):
        try:
            return self.queryset.get(code=self.kwargs['code'])
        except ResetPasword.DoesNotExist:
            raise NotFound("Код не найден")

    def get(self, request, *args, **kwargs):
        reset_password_code = self.get_object()
        if reset_password_code.is_active:
            return get_ok_response("Этот код активен")
        else:
            return Response({"detail": "Этот код не активен"}, status=404)



class LoginByCodeAPIView(GenericAPIView):
    queryset = ResetPasword.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'code'

    def get_object(self):
        try:
            return self.queryset.get(code=self.kwargs['code'])
        
        except ResetPasword.DoesNotExist:
            raise NotFound("Код не найден")

    def get(self, request, *args, **kwargs):
        reset_password_code = self.get_object()
        if reset_password_code:
            current_time = now()
            time_diff = current_time - reset_password_code.date
            if time_diff.total_seconds() < 360:
                user = reset_password_code.user
                token, _ = Token.objects.get_or_create(user=user)
                reset_password_code.delete()
                return Response({"detail":"Login successful","token":token.key})
            
        return Response({"detail": "Этот код не активен"}, status=404)




class ResetPasswordAPIView(ResetPasswordService,GenericAPIView):
    queryset = ResetPasword.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResetPasswordSerializer



class UserModelViewSet(UserModelService,SuperModelViewSet):
    queryset = User.objects.all().prefetch_related('client','client__bonus_card','employees','employees__position')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    search_fields = ['phone','middle_name','email','first_name','last_name']
    ordering_fields = ['id','last_activity','date_joined']
    filterset_class = UserFilterSet
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated,IsSuperAdmin],
        'create': [permissions.IsAuthenticated,IsSuperAdmin],
        'destroy': [permissions.IsAuthenticated,IsSuperAdmin],
        'retrieve':[permissions.IsAuthenticated,IsSuperAdmin],
        'update':[permissions.IsAuthenticated,IsSuperAdmin],
    }
    


class PhoneNumberChangeViewSet(PhoneNumberChangeService,mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = PhoneNumberChange.objects.all()
    serializer_class = PhoneNumberChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'code'

    

class SetPinCodeView(GenericAPIView):
    serializer_class = SetPinCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            pin_code = serializer.validated_data['pin_code']
            request.user.set_pin_code(pin_code)
            return Response({"detail": "PIN-код успешно установлен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyPinCodeView(GenericAPIView):
    serializer_class = VerifyPinCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            pin_code = serializer.validated_data['pin_code']
            if request.user.check_pin_code(pin_code):
                return Response({"detail": "PIN-код верный."}, status=status.HTTP_200_OK)
            return Response({"detail": "Неверный PIN-код."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    