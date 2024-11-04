from rest_framework import serializers

from apps.user.models import User,TariffPlan
from api.country.serializers import RegionSerializer

class TariffPLanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffPlan
        fields = '__all__'


class ShortDescUserSerializer(serializers.ModelSerializer):
    tariff_plan = TariffPLanSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    class Meta:
        model = User
        exclude = (
            'last_activity',
            'password',
            'is_superuser',
            'is_staff',
            'groups',
            'user_permissions'
        )

