from django.db import models

from apps.utils.models import TimeStampAbstractModel
from .constants import IMPORTANCE_CHOICE,LOW,MEDIUM,HIGH,STATUS_CHOICE,PRIMARY,CORRECTED,RECONCILIATORS_STATUS_CHOICE,NOT_CONFIRMED
from apps.user.constants import ROLE_CHOICE,EMPLOYEE
# Create your models here.
class Application(TimeStampAbstractModel):
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

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-id']

    def __str__(self):
        return f"{self.contract_number}-{self.status}"
    


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
    class Meta:
        verbose_name = 'Согласователь'
        verbose_name_plural = 'Согласователи'
        ordering = ['-id']

    def __str__(self):
        return f"{self.application.contract_number}-{self.user}"
