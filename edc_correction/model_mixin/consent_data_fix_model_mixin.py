from django.db import models
from django.core.validators import RegexValidator

from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from django_crypto_fields.fields.firstname_field import FirstnameField
from django_crypto_fields.fields.lastname_field import LastnameField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_constants.choices import GENDER_UNDETERMINED, YES_NO

from ..exceptions import DataFixError
from .data_fix_validation_mixin import DataFixValidationMixin
from .update_value_mixin import UpdateDataValues


class ConsentDataFixModelMixin(DataFixValidationMixin, BaseUuidModel):

    """A model linked to the subject consent to record corrections."""

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    old_first_name = FirstnameField(
        null=True,
        blank=True,
    )

    first_name = FirstnameField(
        null=True,
        blank=True,
    )

    old_last_name = LastnameField(
        null=True,
        blank=True,
    )
    last_name = LastnameField(
        null=True,
        blank=True,
    )

    old_initials = EncryptedCharField(
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
    )

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        blank=True,
    )

    old_dob = models.DateField(
        verbose_name="Old Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    dob = models.DateField(
        verbose_name="New Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    old_gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        blank=True,
        null=True,
        max_length=1)

    gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=True,
    )

    old_guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is '
                           '\'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                           'All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    old_may_store_samples = models.CharField(
        verbose_name="Old Sample storage",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    may_store_samples = models.CharField(
        verbose_name="New Sample storage",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    old_is_literate = models.CharField(
        verbose_name="(Old) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    is_literate = models.CharField(
        verbose_name="(New) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    old_witness_name = LastnameField(
        verbose_name="Witness\'s Last and first name (illiterates only)",
        validators=[
            RegexValidator(
                '^[A-Z]{1,50}\, [A-Z]{1,50}$',
                'Invalid format. Format '
                'is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma')],
        blank=True,
        null=True,
        help_text=('Required only if subject is illiterate. '
                   'Format is \'LASTNAME, FIRSTNAME\'. '
                   'All uppercase separated by a comma'),
    )

    witness_name = LastnameField(
        verbose_name="Witness\'s Last and first name (illiterates only)",
        validators=[
            RegexValidator(
                '^[A-Z]{1,50}\, [A-Z]{1,50}$',
                'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                'All uppercase separated by a comma')],
        blank=True,
        null=True,
        help_text=('Required only if subject is illiterate. '
                   'Format is \'LASTNAME, FIRSTNAME\'. '
                   'All uppercase separated by a comma'),
    )

    is_verified = models.BooleanField(default=False, editable=False)

    is_verified_datetime = models.DateTimeField(null=True, editable=False)

    verified_by = models.CharField(max_length=25, null=True, editable=False)

    def __str__(self):
        return str(self.subject_identifier,)

    def save(self, *args, **kwargs):
        for subject_consent in self.subject_consents:
            self.compare_old_fields_to_db_values(
                subject_consent=subject_consent, exception_cls=DataFixError)
        for subject_consent in self.subject_consents:
            update_data_values = UpdateDataValues(
                consent_data_fix=self, subject_consent=subject_consent,
                first_name=self.first_name, last_name=self.last_name,
                dob=self.dob, initials=self.initials, gender=self.gender,
                guardian_name=self.guardian_name,
                may_store_samples=self.may_store_samples,
                is_literate=self.is_literate, witness_name=self.witness_name)
            update_data_values.update_values()
        super(ConsentDataFixModelMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'edc_correction'
