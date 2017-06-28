from django.conf.urls import url, include
from django.contrib import admin

from edc_base.views import LogoutView, LoginView

from .views import HomeView
from .apps import EdcCorrectionAppConfig

app_name = 'edc_correction'

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #     url(r'^apps', include('apps.urls')),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(
        pattern_name='login_url'), name='logout_url'),
    url(r'', HomeView.as_view(), name='home_url'),
]
