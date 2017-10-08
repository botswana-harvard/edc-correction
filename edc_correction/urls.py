from django.conf.urls import url, include
from django.contrib import admin

from edc_base.views import LogoutView, LoginView

from .admin_site import edc_correction_admin
from .views import HomeView

app_name = 'edc_correction'

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', edc_correction_admin.urls),
    url(r'^edc/', include('edc_base.urls')),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'logout', LogoutView.as_view(
        pattern_name='login_url'), name='logout_url'),
    url(r'', HomeView.as_view(), name='home_url'),
]
