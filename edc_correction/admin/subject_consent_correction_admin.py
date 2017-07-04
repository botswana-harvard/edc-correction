from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from ..forms import SubjectConsentCorrectionForm
from ..models import SubjectConsentCorrection


@admin.register(SubjectConsentCorrection)
class SubjectConsentCorrectionAdmin(admin.ModelAdmin):

    form = SubjectConsentCorrectionForm

    fieldsets = (
        ('For completion by TMG Investigator Only', {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'first_name',
                'new_first_name',
                'last_name',
                'new_last_name',
                'initials',
                'new_initials',
                'dob',
                'new_dob',
                'gender',
                'new_gender',
                'guardian_name',
                'new_guardian_name',
                'may_store_samples',
                'new_may_store_samples',
                'is_literate',
                'witness_name',
                'new_witness_name'
            )}),
        audit_fieldset_tuple
    )

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                + audit_fields)
