from django.contrib import admin
from .models import WalletHistory, Beneficiary, AddFund, PaymentOption, Withdrawal, FundRequest
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import csv
from django.http import HttpResponse

from users.models import User
from import_export import resources
from import_export.admin import ImportExportMixin
# Register your models here.
class WalletResource(resources.ModelResource):
    class Meta:
        model = WalletHistory
        fields = [f.name for f in WalletHistory._meta.fields]

class WalletAdmin(ImportExportModelAdmin):
    resource_class = WalletResource
    list_display = [f.name for f in WalletHistory._meta.fields]
    search_fields = ('user_id', 'amount', 'comment', )

admin.site.register(WalletHistory, WalletAdmin)

class BeneficiaryResource(resources.ModelResource):
    class Meta:
        model = Beneficiary
        fields = [f.name for f in Beneficiary._meta.fields]


class BeneficiaryAdmin(ImportExportModelAdmin):
    resource_class = BeneficiaryResource
    list_display = [f.name for f in Beneficiary._meta.fields]

class AddFundAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AddFund._meta.fields]

class accountsAdmin(admin.ModelAdmin):
    search_fields = ('user', )
    list_display = [f.name for f in PaymentOption._meta.fields]
    readonly_fields = ( 'verification', )

class withdrawalAdmin(admin.ModelAdmin):
    search_fields = ('user', )
    list_display = [f.name for f in Withdrawal._meta.fields]
    list_editable = ('status',)
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = ('user', 'name', 'total_amount', 'ifsc', 'account_number', )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(PaymentOption, accountsAdmin)

admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(AddFund, AddFundAdmin)
admin.site.register(Withdrawal, withdrawalAdmin)
admin.site.register(FundRequest)