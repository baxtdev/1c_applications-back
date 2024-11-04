from rest_registration.api.views.login import Response
from rest_registration.api.views.profile import ProfileView

from rest_framework.authtoken.models import Token

from api.user.serializers import UserSerializer,User


class CustomProfileView(ProfileView):
    
    def delete(self, request, *args, **kwargs)-> Response:
        user:User = request.user
        user.is_active = False
        user.delete()
        return Response({"detail": "Профиль был удален."}, status=204)