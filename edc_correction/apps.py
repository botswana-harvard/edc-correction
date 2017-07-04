from django.apps import AppConfig


class EdcCorrectionAppConfig(AppConfig):
    name = 'edc_correction'
    url_namespace = 'edc_correction'

    def ready(self):
        pass
