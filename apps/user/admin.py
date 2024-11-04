from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _


from .models import User,ResetPasword,PhoneNumberChange



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('get_full_name','id','role')
    readonly_fields = ['last_login']
    list_filter = ['role','is_superuser','is_active','is_staff']
    fieldsets = (
        (None, {'fields': (
            'username',
            'phone',
            'password',
        )}),
        (_('Personal info'), {'fields': (
            'image',
            'first_name',
            'last_name',
            'middle_name',
            'role',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_notifications',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
        )}),
    )    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'role'
            ),
        }),
    )
    search_fields = ['first_name', 'last_name']
    ordering = ['id']
  

@admin.register(ResetPasword)
class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('user','is_active','code','date')


@admin.register(PhoneNumberChange)
class PhoneNumberChangeAdmin(admin.ModelAdmin):
    list_display = ('user','is_active','new_phone_number','code','created_at')

    