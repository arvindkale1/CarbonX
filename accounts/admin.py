from django.contrib import admin
from .models import Profile, DematAccount, Transaction, CarbonCreditType

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved')
    list_editable = ('is_approved',)

@admin.register(DematAccount)
class DematAdmin(admin.ModelAdmin):
    list_display = ('user', 'credit_balance', 'wallet_balance')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'credit_type', 'credits', 'amount', 'date')

@admin.register(CarbonCreditType)
class CreditTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_credit')
