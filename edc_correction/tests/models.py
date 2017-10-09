from django.db import models

from edc_base.model_mixins import BaseUuidModel
from django.core.validators import RegexValidator

from edc_constants.choices import GENDER_UNDETERMINED, YES_NO
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from django_crypto_fields.fields.lastname_field import LastnameField
from django_crypto_fields.fields.firstname_field import FirstnameField
from edc_base.model_validators.date import datetime_not_future
from ..model_mixin import ConsentDataFixModelMixin


class SubjectConsent(BaseUuidModel):

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

    first_name = FirstnameField(
        null=True,
        blank=True,
    )

    last_name = LastnameField(
        null=True,
        blank=True,
    )

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        blank=True,
    )

    dob = models.DateField(
        verbose_name="New Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=True,
    )

    guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                           'All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    may_store_samples = models.CharField(
        verbose_name="New Sample storage",
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

    class Meta:
        app_label = 'edc_correction'
