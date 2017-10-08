from django import forms

from edc_base.modelform_mixins import JSONModelFormMixin, CommonCleanModelFormMixin
from edc_base.modelform_validators import FormValidatorMixin

from ..models import ConsentDataFix


class ConsentDataFixForm(FormValidatorMixin, CommonCleanModelFormMixin,
                         JSONModelFormMixin, forms.ModelForm):

    class Meta:
        model = ConsentDataFix
        fields = '__all__'
