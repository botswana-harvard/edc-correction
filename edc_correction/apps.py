from django.apps import apps as django_apps
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from edc_base.utils import age


class AppConfig(DjangoAppConfig):
    name = 'edc_correction'

    consent_model = 'edc_correction.subjectconsent'
    dt_fixible_model_label_lowers = ['edc_correction.datafixtestmodel']
    age_min = 16
    age_is_adult = 18
    age_max = 64
    age

    @property
    def data_fixible_models(self):
        model_classes = []
        for lable_lower in self.dt_fixible_model_label_lowers:
            model_classes.append(
                django_apps.get_model(lable_lower)._meta.object_name)
        return model_classes


if 'edc_correction' in settings.APP_NAME:
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol_title = 'EDC Correction'
