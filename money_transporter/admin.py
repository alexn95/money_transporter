from django.contrib import admin

from money_transporter import  models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'currency', 'balance', 'is_staff', 'is_superuser')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_datetime',)
    list_display = ('sender', 'recipient', 'create_datetime')
