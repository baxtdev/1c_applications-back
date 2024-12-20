from django.db.transaction import atomic

from rest_framework import serializers

from django_base64field.fields import Base64Field

from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.application.models import Application,ApplicationPayment,ApplicationReconciliators,ApplicationTotalAmount,\
    RECONCILIATORS_STATUS_CHOICE,NOT_CONFIRMED,CONFIRMED,CANCELED,ApplicationDocument
from apps.utils.utils import get_filter_object_or_none
from apps.utils.fields import Base64FileField
from apps.utils.serializers import ShortDescUserSerializer

class ApplicationPaymentSerializer(serializers.ModelSerializer):
    payment_amount = serializers.FloatField(read_only=True)
    remaining_amount = serializers.FloatField(read_only=True)
    class Meta:
        model = ApplicationPayment
        exclude = ['application']
        read_only_fields = ['remaining_amount','payment_amount']


class ApplicationCreatePaymentSerializer(serializers.ModelSerializer):
    payment_amount = serializers.FloatField(read_only=True)
    remaining_amount = serializers.FloatField(read_only=True)
    class Meta:
        model = ApplicationPayment
        fields = '__all__'
        read_only_fields = ['remaining_amount','payment_amount']



class ApplicationReconciliatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationReconciliators
        exclude = ['application']


class ApplicationReconciliatorsListSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()
    class Meta:
        model = ApplicationReconciliators
        exclude = ['application']


class ApplicationReconciliatorsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationReconciliators
        fields = '__all__'

class ApplicationTotalAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationTotalAmount
        exclude = ['application']


class ApplicationTotalAmountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationTotalAmount
        fields = '__all__'


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    document = Base64FileField()
    class Meta:
        model = ApplicationDocument
        exclude = ['application']



class ApplicationDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = '__all__'


class ApplicationSerializer(WritableNestedModelSerializer):
    payments = ApplicationPaymentSerializer(many=True,required=False)
    reconciliators = ApplicationReconciliatorsSerializer(many=True,required=True)
    total_amounts = ApplicationTotalAmountSerializer(many=True,required=False)
    documents = ApplicationDocumentSerializer(many=True,required=False)
    total_price_without_VAT = serializers.FloatField()
    total_price = serializers.FloatField()
    total_rate_VAT = serializers.FloatField()
    total_amount_VAT = serializers.FloatField()
    remaining_amount = serializers.FloatField()
    paid_amount = serializers.FloatField()
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('total_price','total_price_without_VAT','total_rate_VAT','total_amount_VAT','remaining_amount','paid_amount')




class ApplicationListSerializer(WritableNestedModelSerializer):
    payments = ApplicationPaymentSerializer(many=True,required=False)
    reconciliators = ApplicationReconciliatorsListSerializer(many=True,required=True)
    total_amounts = ApplicationTotalAmountSerializer(many=True,required=False)
    documents = ApplicationDocumentSerializer(many=True,required=False)
    total_price_without_VAT = serializers.FloatField()
    total_price = serializers.FloatField()
    total_rate_VAT = serializers.FloatField()
    total_amount_VAT = serializers.FloatField()
    remaining_amount = serializers.FloatField()
    paid_amount = serializers.FloatField()
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('total_price','total_price_without_VAT','total_rate_VAT','total_amount_VAT','remaining_amount','paid_amount')



class ApplicationCreateSerializer(serializers.ModelSerializer):
    payments = ApplicationPaymentSerializer(many=True,required=True)
    reconciliators = ApplicationReconciliatorsSerializer(many=True,required=True)
    total_amounts = ApplicationTotalAmountSerializer(many=True,required=True)
    documents = ApplicationDocumentSerializer(many=True,required=False)
    total_price_without_VAT = serializers.FloatField()
    total_price = serializers.FloatField()
    total_rate_VAT = serializers.FloatField()
    total_amount_VAT = serializers.FloatField()
    remaining_amount = serializers.FloatField()
    paid_amount = serializers.FloatField()
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('total_price','total_price_without_VAT','total_rate_VAT','total_amount_VAT','remaining_amount','paid_amount')


    @atomic
    def create(self, validated_data):
        payments = validated_data.pop('payments')
        reconciliators = validated_data.pop('reconciliators')
        total_amounts = validated_data.pop('total_amounts')
        documents = validated_data.pop('documents')
        application = Application.objects.create(**validated_data)
        
        for payment in payments:
            application.payments.create(**payment)
        
        for reconciliator in reconciliators:    
            application.reconciliators.create(**reconciliator)
        
        for total_amount in total_amounts:    
            application.total_amounts.create(**total_amount)

        for document in documents:
            application.documents.create(**document)
       
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
    

class ApplicationStatusChange(serializers.Serializer):
   application = serializers.PrimaryKeyRelatedField(
        queryset=Application.objects.all(),
        required=True,
   )
   status = serializers.ChoiceField(choices=RECONCILIATORS_STATUS_CHOICE, required=True)

   def validate_status(self, value):
       if value == NOT_CONFIRMED:
           raise serializers.ValidationError('Нельзя изменить статус на Не подтвержден')
       return value
   
   def validate(self, attrs):
       user = self.context['request'].user
       application = attrs.get('application')
       try: 
            application_reconciliators = application.reconciliators.filter(user=user).first()
            application_reconciliators_not_confirmed = application.reconciliators.filter(
                status__in=[NOT_CONFIRMED,CANCELED],
                sequence_hierarchy__lt=application_reconciliators.sequence_hierarchy
            )
            if application_reconciliators_not_confirmed.exists():
                raise serializers.ValidationError({'application':'Необходимо подтвердить заявку другие согласователи'})
            
            if application_reconciliators.status == attrs.get('status'):
                raise serializers.ValidationError({'status':'Статус заявки уже установлен'})

            attrs['application_reconciliators']=application_reconciliators
            return super().validate(attrs)
            
       except AttributeError:
           raise serializers.ValidationError({'detail':'Вы не являетесь администратором данного приложения'})   
          
   def create(self, validated_data):
       application_reconciliators = validated_data.get('application_reconciliators')
       status = validated_data.get('status')
       application = validated_data.get('application')
       application_reconciliators.status = status
       application_reconciliators.save()
       return application
       

