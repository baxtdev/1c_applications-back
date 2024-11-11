from django.contrib import admin

# Register your models here.
from .models import Application,ApplicationPayment,ApplicationReconciliators,ApplicationTotalAmount,ApplicationDocument



class ApplicationPaymentInline(admin.TabularInline):
    model = ApplicationPayment
    extra = 0
    show_change_link = True



class ApplicationReconciliatorsInline(admin.TabularInline):
    model = ApplicationReconciliators
    extra = 0
    show_change_link = True



class ApplicationTotalAmountInline(admin.StackedInline):
    model = ApplicationTotalAmount
    extra = 0
    show_change_link = True


class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0
    show_change_link = True



@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id','contract_number','importance', 'status', 'created_date', 'supplier', 'initiator',)
    list_filter = ('importance', 'status', 'created_date')
    list_display_links = ('id','importance','contract_number')
    search_fields = ('supplier', 'initiator', 'contract_number')
    ordering = ['created_date']
    inlines = [ApplicationTotalAmountInline,ApplicationPaymentInline, ApplicationReconciliatorsInline,ApplicationDocumentInline]


@admin.register(ApplicationPayment)
class ApplicationPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'payment_percentage_amount', 'payment_date', 'payment_method')
    list_filter = ('payment_date','application')
    search_fields = ('application__contract_number','payment_method')
    ordering = ['payment_date','id']


@admin.register(ApplicationReconciliators)
class ApplicationReconciliatorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'user', 'status')
    list_filter = ('status','application','user__role')
    search_fields = ('application__contract_number','user')
    ordering = ['application']



@admin.register(ApplicationTotalAmount)
class ApplicationTotalAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'budget_code','direction','nomenclature','price')
    list_filter = ('application',)
    search_fields = ('application__contract_number',)
    ordering = ['application','id']


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('id','document_name','document')
    search_fields = ('document','document_name')

