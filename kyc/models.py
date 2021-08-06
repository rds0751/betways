from django.db import models
from django.utils.html import escape
from django.utils.html import mark_safe

# Create your models here.
class ImageUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=20, unique=True)
    imageAF = models.ImageField()
    imageAB = models.ImageField()
    name = models.CharField(max_length=100, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.NullBooleanField(null=True)
    
    def __str__(self):
        return self.user

    def pan_image(self):
        return mark_safe('<img src="{}" width="400" />'.format(self.imageP.url))

    def aadhar_front(self):
        return mark_safe('<img src="{}" width="400" />'.format(self.imageAF.url))

    def aadhar_back(self):
        return mark_safe('<img src="{}" width="400" />'.format(self.imageAB.url))