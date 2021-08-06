from django.conf.urls import url 
from .views import ocr_core
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^pancard/$', ocr_core, name='PanCard'), #PAN Card OCR template!
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

