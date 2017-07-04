from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from django.contrib import admin

from ..forms import SubjectConsentCorrectionForm
from ..models import SubjectConsentCorrection


@admin.register(SubjectConsentCorrection)
class SubjectConsentCorrectionAdmin(admin.ModelAdmin):

    form = SubjectConsentCorrectionForm

    fieldsets = (
        ('For completion by Authorized Persons Only', {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'old_first_name',
                'new_first_name',
                'old_last_name',
                'new_last_name',
                'old_initials',
                'new_initials',
                'old_dob',
                'new_dob',
                'old_gender',
                'new_gender',
                'old_guardian_name',
                'new_guardian_name',
                'old_may_store_samples',
                'new_may_store_samples',
                'old_is_literate',
                'new_is_literate',
                'old_witness_name',
                'new_witness_name'
            )}),
        audit_fieldset_tuple
    )

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                + audit_fields)
