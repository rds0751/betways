from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# get a way to log the errors:
import logging
log = logging.getLogger(__name__)
# convert the errors to text
from django.utils.encoding import force_text

from users.models import User
from import_export import resources
from .models import User
import csv
from django.http import HttpResponse
from import_export.admin import ImportExportMixin

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = [f.name for f in User._meta.fields]

class MyUser1CreationForm(UserCreationForm):
    recharge_limit = forms.FloatField(required = False)
    income = forms.FloatField(required = False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def is_valid(self):
        log.info(force_text(self.errors))
        return super(MyUser1CreationForm, self).is_valid()

class MyUser1ChangeForm(UserChangeForm):
    recharge_limit = forms.FloatField(required = False)
    binary_income = forms.FloatField(required = False)
    income = forms.FloatField(required = False)
    new_funds = forms.FloatField(required=False)
    referal = forms.CharField(required = False)
    shopping_wallet = forms.FloatField(required=False)
    recharge_limit = forms.FloatField(required=False)
    added_amount = forms.FloatField(required=False)
    total_income = forms.FloatField(required=False)

    class Meta:
        model = User
        fields = [f.name for f in User._meta.fields]

    def is_valid(self):
        log.info(force_text(self.errors))
        return super(MyUser1ChangeForm, self).is_valid()


class UserAdmin(UserAdmin):
    resource_class = UserResource
    search_fields = ('name', 'mobile', 'username', 'email', )
    form = MyUser1ChangeForm
    add_form = MyUser1CreationForm
    list_display = ('username', 'name', 'referral', 'mobile', 'email', 'is_active', 'otp', )
    list_editable = ('is_active', )

    def change_view(self, request, object_id):
        if request.user.is_superuser:
            self.fieldsets = (
                    (None, {'fields': ('username', 'password', )}),
                    (_('Personal info'), {'fields': ( 'name', 'email', 'mobile', )}),
                    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'user_permissions', )}),
                    (_('Important dates'), {'fields': ('last_login', )}),
                    (_('Groups'), {'fields': ('groups',)}),
                )
        else:
            self.fieldsets = (
                    (None, {'fields': ('username', 'password', )}),
                    (_('Personal info'), {'fields': ( 'name', 'email', 'mobile', )}),
                    (_('Important dates'), {'fields': ('last_login', )}),
                )
        return super(UserAdmin, self).change_view(request, object_id,)

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = ('name', 'email', )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    actions = [export_as_csv]
    export_as_csv.short_description = "Export Selected"

admin.site.register(User, UserAdmin)