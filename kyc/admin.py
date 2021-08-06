from django.contrib import admin
from .models import ImageUploadModel
# Register your models here.


class kycAdmin(admin.ModelAdmin):
	search_fields = ('user', )
	list_display = [f.name for f in ImageUploadModel._meta.fields]
	fields = ['aadhar_front', 'aadhar_back', 'description', 'name', 'approved', ]
	readonly_fields = ('aadhar_back', 'aadhar_front', )

admin.site.register(ImageUploadModel, kycAdmin)