from django.db import models

from apps.utils.models import TimeStampAbstractModel
from .constants import *
from apps.user.constants import ROLE_CHOICE,EMPLOYEE
# Create your models here.
class Application(TimeStampAbstractModel):
    application_type = models.CharField(
        verbose_name="тип заявки",
        max_length=300,
        blank=True,
        null=True
    )
    importance = models.CharField(
        max_length=255,
        choices=IMPORTANCE_CHOICE,
        default=LOW,
        verbose_name='Важность заявки'
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICE,
        default=PRIMARY,
        verbose_name='Статус заявки'
    )
    current_status = models.CharField(
        max_length=255,
        verbose_name='Текущий статус',
        choices=RECONCILIATORS_STATUS_CHOICE,
        default=NOT_CONFIRMED,
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания заявки',
    )
    supplier = models.CharField(
        max_length=300,
        verbose_name='Поставщик'
    )
    initiator = models.CharField(
        max_length=255,
        verbose_name='Инициатор заявки'
    )
    contract_number = models.CharField(
        max_length=255,
        verbose_name='Номер договора',
        unique=True
    )
    purchase_reconciliations_status = models.CharField(
        max_length=255,
        verbose_name='Текущий статус от закупа',
        choices=RECONCILIATORS_STATUS_CHOICE,
        default=NOT_CONFIRMED,
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-id']

    def __str__(self):
        return f"{self.contract_number}-{self.status}"
    

    def _to_chek_reconciliations_statuses(self):
        if self.reconciliators.filter(status=CONFIRMED).count()==self.reconciliators.count():
            status = CONFIRMED == self.purchase_reconciliations_status
            self.current_status = status
    
    def _to_chek_purchase_reconciliations_status(self):
        if self.purchase_reconciliations.filter(status=CONFIRMED).count()==self.purchase_reconciliations.count():
            self.purchase_reconciliations_status = CONFIRMED
            first_reconciliator = self.reconciliators.order_by('sequence_hierarchy').first()
            if first_reconciliator:
                first_reconciliator.is_current = True
                first_reconciliator.save(update_fields=['is_current'])


    def cancel_material_for_purchase(self,material,quantity_agreed,user):
        if not self.purchase_reconciliations.filter(user=user).exists(): 
            raise ValueError({"detail":"Этот пользователь не имеет права"})
        
        if not material.application == self:
            raise ValueError({"detail":"Этот материал не принадлежить этой заявки"})
        
        if material.quantity_agreed == quantity_agreed:
            raise ValueError({"detail":"Нельзя отменить заявку с равным количеством"})
        
        if material.quantity_agreed < quantity_agreed:
            raise ValueError({"detail":"Нельзя отменить заявку с больщим количнством"})
        
        if material.quantity_agreed <0:
            raise ValueError({"detail":"Нельзя отменить заявку с больщим количнством"})
        
        material.status = NOT_CONFIRMED
        material.quantity_agreed = quantity_agreed
        material.canceled_from_user = user
        material.save(update_fields=['status','quantity_agreed','canceled_from_user'])


    @property
    def total_price(self):
        return sum(amount.price for amount in self.total_amounts.all())
    total_price.fget.short_description = "Общая цена"

    @property
    def total_price_without_VAT(self):
        return sum(amount.price_without_VAT for amount in self.total_amounts.all())
        # return sum(amount.price for amount in self.total_amounts.all()) * (1 - sum(amount.VAT_rate for amount in self.total_amounts.all())/100)
        # return sum(amount.price * (1 - amount.VAT_rate/100) for amount in self.total_amounts.all())

    total_price_without_VAT.fget.short_description = "Общая цена без НДС"

    @property
    def total_rate_VAT(self):
        return sum(amount.VAT_rate for amount in self.total_amounts.all())

    total_rate_VAT.fget.short_description = "Общая ставка НДС"

    @property
    def total_amount_VAT(self):
        return sum(amount.VAT_amount for amount in self.total_amounts.all())
    total_amount_VAT.fget.short_description = "Общая сумма НДС"

    @property
    def remaining_amount(self):
        return self.total_price - sum(payment.payment_amount for payment in self.payments.all())
    remaining_amount.fget.short_description = "Оставшая сумма"

    @property
    def paid_amount(self):
        return sum(payment.payment_amount for payment in self.payments.all())
    paid_amount.fget.short_description = "Сумма оплаты"


class ApplicationTotalAmount(TimeStampAbstractModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='total_amounts',
    )
    budget_code  = models.CharField(
        max_length=255,
        verbose_name='Код бюджета',
        unique=True
    )
    direction = models.CharField(
        max_length=255,
        verbose_name='Направление',
    )
    object = models.CharField(
        max_length=255,
        verbose_name='Объект',
    )
    nomenclature = models.CharField(
        max_length=500,
        verbose_name='Номенклатура',
    )
    unit_of_measurement = models.CharField(
        max_length=255,
        verbose_name='Единица измерения',
    )
    price = models.FloatField(
        verbose_name='Цена',
        default=0
    )
    quantity = models.FloatField(
        verbose_name='Количество',
        default=0
    )
    VAT_rate = models.FloatField(
        verbose_name='Ставка НДС (в процентах %)',
        default=0
    )
    VAT_amount = models.FloatField(
        verbose_name='Сумма НДС',
        default=0
    )

    class Meta:
        verbose_name = 'Сумма ИТОГО'
        verbose_name_plural = 'Суммы ИТОГИ'
        ordering = ['-id']

    def __str__(self):
        return f"{self.application.contract_number}-{self.budget_code}"
    
    @property
    def price_without_VAT(self):
        return self.price * (1 - self.VAT_rate/100)


class ApplicationPayment(TimeStampAbstractModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    payment_date = models.DateField(
        verbose_name='Дата оплаты',
    )
    payment_percentage_amount = models.FloatField(
        verbose_name='Процент от Сумма оплаты (в процентах %)',
        default=0,
    )
    payment_method = models.CharField(
        max_length=255,
        verbose_name='Метод оплаты',
        default='Безналичный расчет',
        blank=True,
        null=True,
    )
    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-id']

    def __str__(self):
        return f"{self.application.contract_number}-{self.payment_percentage_amount}"   

    @property
    def payment_amount(self):
        return self.payment_percentage_amount * self.application.total_price / 100
    payment_amount.fget.short_description = "Сумма"

    @property
    def remaining_amount(self):
        return self.application.remaining_amount
    
    @property
    def paid_amount(self):
        return self.application.paid_amount




class ApplicationReconciliators(TimeStampAbstractModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='reconciliators',
        verbose_name='Заявка'
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='reconciliations',
        verbose_name='Согласователь'
    )
    role = models.CharField(
        max_length=255,
        verbose_name='Роль',
        choices=ROLE_CHOICE,
        default=EMPLOYEE,
    )
    sequence_hierarchy = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер в иерархии',
        default=1
    )
    status = models.CharField(
        max_length=255,
        choices=RECONCILIATORS_STATUS_CHOICE,
        default=NOT_CONFIRMED,
        verbose_name='Статус'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True
    )
    is_current = models.BooleanField(
        verbose_name='Текущий согласователь',
        default=False,
    )
    class Meta:
        verbose_name = 'Согласователь'
        verbose_name_plural = 'Согласователи'
        ordering = ['-id']

    def __str__(self):
        return f"{self.application.contract_number}-{self.user}"


class ApplicationDocument(TimeStampAbstractModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="заявка"
    )
    document_name = models.CharField(
        verbose_name="Название файла",
        blank=True,
        null=True,
        max_length=250
    )
    document = models.FileField(
        verbose_name="Документ (файл)",
        upload_to="application/documents/",
    )

    class Meta:
        verbose_name = "Документ заявок"
        verbose_name_plural = "Документы заявок"
        ordering = ['-id']

    def __str__(self):
        return f"{self.document.name}"   
     




class ApplicactionMaterial(TimeStampAbstractModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Заявка"
    )
    number = models.CharField(
        verbose_name="Номер (Материала||Услуг)",
        max_length=500
    )
    type = models.CharField(
        verbose_name="Тип",
        max_length=15,
        choices=MATERIAL_TYPE,
        default=MATERIAL
    )
    unit_of_measurement = models.CharField(
        verbose_name="Единица Измерения",
        max_length=200
    )
    quantity = models.FloatField(
        verbose_name="Количество",
        default=0
    )
    brand = models.CharField(
        verbose_name="Марка",
        max_length=250,
    )
    budget_code = models.CharField(
        verbose_name="Бюджетный код",
        max_length=250
    )
    status = models.CharField(
        verbose_name="Статус",
        choices=RECONCILIATORS_STATUS_CHOICE,
        default=NOT_CONFIRMED,
        max_length=100
    )
    quantity_agreed = models.FloatField(
        verbose_name="Согласованное количество",
        blank=True,
        null=True,
        default=0
    )
    canceled_from_user = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        related_name='canceled_materials',
        verbose_name='Отменено от пользователя',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Материал Заявки"
        verbose_name_plural = "Материалы Заявки"
        ordering = ['-id']
    
    def  __str__(self):
        return f"{self.budget_code}-{self.application.contract_number}"


    def cancel_material_for_purchase(self,quantity_agreed,user):
        material = self
        if not self.application.purchase_reconciliations.filter(user=user).exists(): 
            raise ValueError({"detail":"Этот пользователь не имеет права"})
        
        if material.quantity == quantity_agreed:
            raise ValueError({"detail":"Нельзя отменить заявку с равным количеством"})
        
        if material.quantity < quantity_agreed:
            raise ValueError({"detail":"Нельзя отменить заявку с больщим количнством"})
        
        if material.quantity_agreed <0:
            raise ValueError({"detail":"Нельзя отменить заявку с больщим количнством"})
        
        material.status = CANCELED
        material.quantity_agreed = quantity_agreed
        material.canceled_from_user = user
        material.save(update_fields=['status','quantity_agreed','canceled_from_user'])
        self._cancel_for_purchase_reconciliators()

    def _cancel_for_purchase_reconciliators(self):
        reconciliator = self.application.purchase_reconciliations.filter(user=self.canceled_from_user).first()
        reconciliator.status = CANCELED
        reconciliator.save(update_fields=['status'])


class ApplicationPurchaseReconciliators(TimeStampAbstractModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='purchase_reconciliations',
        verbose_name='Заявка'
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='purchase_reconciliations',
        verbose_name='Согласователь'
    )
    role = models.CharField(
        max_length=255,
        verbose_name='Роль',
        choices=ROLE_CHOICE,
        default=EMPLOYEE,
    )
    sequence_hierarchy = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер в иерархии',
        default=1
    )
    status = models.CharField(
        max_length=255,
        choices=RECONCILIATORS_STATUS_CHOICE,
        default=NOT_CONFIRMED,
        verbose_name='Статус'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True
    )
    is_current = models.BooleanField(
        verbose_name='Текущий согласователь',
        default=False,
    )
    class Meta:
        verbose_name = 'Согласователь Закупа'
        verbose_name_plural = 'Согласователи Закупа'
        ordering = ['-id']

    def __str__(self):
        return f"{self.application.contract_number}-{self.user}"