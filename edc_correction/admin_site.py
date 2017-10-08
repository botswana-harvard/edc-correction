from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'EDC Correction'
    site_header = 'EDC Correction'
    index_title = 'EDC Correction'
    site_url = '/edc_correction/list/'


edc_correction_admin = AdminSite(name='edc_correction_admin')
