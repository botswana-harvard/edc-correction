from .model_mixin import ConsentDataFixModelMixin


class ConsentDataFix(ConsentDataFixModelMixin):

    class Meta:
        app_label = 'edc_correction'
