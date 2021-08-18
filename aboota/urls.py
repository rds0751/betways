from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.apps import apps
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from debug_toolbar import urls as durls
from django.conf.urls import re_path
from users import views
from allauth.account.views import LoginView, SignupView

handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'
handler403 = 'home.views.error_403'
handler400 = 'home.views.error_400'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tickets/', include('ticket.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    path('panel/', include('panel.urls', namespace="panel")),
    path("signup/onboarding/", views.signuponboarding, name="signup-onboarding"),
    path('accounts/', include("allauth.urls")),
    url(r'^customurl/login/', LoginView.as_view(template_name='account/login2.html'), name="custom_login" ),
    url(r'^kyc/', include('kyc.urls')),
    path('__debug__/', include(durls), name='debug_toolbar'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('wallet/', include('wallets.urls', namespace="wallet")),
    path('order/', include(('orders.urls', 'orders'), namespace='orders')),
    url(r'api/', include('api.urls')),
    url(r"register=(?P<use>\w{0,50})/", views.referalsignup, name="refersignup"),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('plan/', RedirectView.as_view(url=staticfiles_storage.url("IPM_23July_Final_Presentation-1.pdf")),),
    path('soon/', TemplateView.as_view(template_name='users/coming_soon.html')),
    path('', include('users.urls', namespace="users")),
    path('level/', include('level.urls', namespace="level")),
    path('search/', include("search.urls", namespace="searchy")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('games/', include('games.urls', namespace="games")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]