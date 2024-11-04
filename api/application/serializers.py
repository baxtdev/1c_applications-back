from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.application.models import Application,ApplicationPayment,ApplicationReconciliators,ApplicationTotalAmount


class ApplicationPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationPayment
        exclude = ['application']


class ApplicationReconciliatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationReconciliators
        exclude = ['application']


class ApplicationTotalAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationTotalAmount
        exclude = ['application']


class ApplicationSerializer(WritableNestedModelSerializer):
    payments = ApplicationPaymentSerializer(many=True)
    reconciliators = ApplicationReconciliatorsSerializer(many=True)
    total_amounts = ApplicationTotalAmountSerializer(many=True)
    class Meta:
        model = Application
        fields = '__all__'



