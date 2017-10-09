from django.contrib import admin

from .admin_site import edc_correction_admin
from edc_base.modeladmin_mixins import audit_fieldset_tuple


from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from .forms import ConsentDataFixForm
from .models import ConsentDataFix


@admin.register(ConsentDataFix, site=edc_correction_admin)
class ConsentDataFixAdmin(ModelAdminNextUrlRedirectMixin,
                          ModelAdminFormInstructionsMixin,
                          ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                          ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                          ModelAdminInstitutionMixin, admin.ModelAdmin):

    form = ConsentDataFixForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'old_first_name',
                'first_name',
                'old_last_name',
                'last_name',
                'old_initials',
                'initials',
                'old_dob',
                'dob',
                'old_gender',
                'gender',
                'old_guardian_name',
                'guardian_name',
                'old_may_store_samples',
                'may_store_samples',
                'old_is_literate',
                'is_literate',
                'old_witness_name',
                'witness_name',)}),
        audit_fieldset_tuple)

    radio_fields = {
        "gender": admin.VERTICAL,
        "old_gender": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "old_is_literate": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        "old_may_store_samples": admin.VERTICAL,
    }

    instructions = ['Complete this form once per day.']
