from django.db.transaction import atomic

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
    payments = ApplicationPaymentSerializer(many=True,required=True)
    reconciliators = ApplicationReconciliatorsSerializer(many=True,required=True)
    total_amounts = ApplicationTotalAmountSerializer(many=True,required=True)
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationCreateSerializer(serializers.ModelSerializer):
    payments = ApplicationPaymentSerializer(many=True,required=True)
    reconciliators = ApplicationReconciliatorsSerializer(many=True,required=True)
    total_amounts = ApplicationTotalAmountSerializer(many=True,required=True)
    
    class Meta:
        model = Application
        fields = '__all__'

    @atomic
    def create(self, validated_data):
        payments = validated_data.pop('payments')
        reconciliators = validated_data.pop('reconciliators')
        total_amounts = validated_data.pop('total_amounts')
        application = Application.objects.create(**validated_data)
        
        for payment in payments:
            application.payments.create(**payment)
        
        for reconciliator in reconciliators:    
            application.reconciliators.create(**reconciliator)
        
        for total_amount in total_amounts:    
            application.total_amounts.create(**total_amount)

       
        return application

    @atomic
    def update(self, instance, validated_data):
        payments = validated_data.pop('payments', None)
        reconciliators = validated_data.pop('reconciliators', None)
        total_amounts = validated_data.pop('total_amounts', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if payments is not None:
            instance.payments.all().delete()  
            for payment in payments:
                instance.payments.create(**payment)  

        if reconciliators is not None:
            instance.reconciliators.all().delete()  
            for reconciliator in reconciliators:
                instance.reconciliators.create(**reconciliator)  

        if total_amounts is not None:
            instance.total_amounts.all().delete() 
            for total_amount in total_amounts:
                instance.total_amounts.create(**total_amount)  

        return instance 
    
