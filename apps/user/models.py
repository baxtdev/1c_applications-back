from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password,check_password


from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from apps.utils.models import TimeStampAbstractModel
from apps.utils.utils import generate_code,generate_string_code,generate_barcode
from .managers import UserManager
from .constants import ROLE_CHOICE,EMPLOYEE,ADMIN,OBSERVER,MAIN_EMPLOYEE


class User(AbstractUser):
    image = ResizedImageField(
        upload_to='avatars/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    ) 
    middle_name = models.CharField(
        max_length=255, 
        verbose_name='Отчество',
        blank=True,
        null=True
        )
    role = models.CharField(
        choices = ROLE_CHOICE,
        max_length = 50,
        default = EMPLOYEE,
        verbose_name="Рол"
    )
    
    class Meta:
        db_table = 'main_table'
        managed = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    @property
    def get_full_name(self) -> str:
        return self.username

    def __str__(self) -> str:
        return f"{self.username}-{self.role}"



class ResetPasword(TimeStampAbstractModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='codes',
    )
    is_active = models.BooleanField()
    code = models.IntegerField(
        unique=True,
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        auto_created=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        code = generate_code()
        if not self.code:
            self.code = code
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.phone}--{self.code}"
        
    class Meta:
        db_table = 'codes_res_password_table'
        managed = True
        verbose_name = 'Код для сброса пароля'
        verbose_name_plural = 'Коды для  сброса пароля'  
        ordering = ['-id']



class PhoneNumberChange(TimeStampAbstractModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
    )
    is_active = models.BooleanField(
        default=True
    )
    new_phone_number = PhoneNumberField(
        max_length=20,
        unique=True,
    )
    code = models.IntegerField(
        unique=True,
        default=generate_code
    )

    class Meta:
        verbose_name = 'Код для изменение номер телефона'
        verbose_name_plural = 'Коды для изменение номер телефона'
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.user.get_full_name}-{self.new_phone_number}-{self.code}"    
    


