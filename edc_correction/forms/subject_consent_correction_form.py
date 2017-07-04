# from .form_mixins import SubjectModelFormMixin
from django import forms

from ..models import SubjectConsentCorrection


class SubjectConsentCorrectionForm(forms.ModelForm):

    class Meta:
        model = SubjectConsentCorrection
        fields = '__all__'
