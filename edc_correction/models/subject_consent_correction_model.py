from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future

from django.core.validators import RegexValidator
from django.db import models

from . import CorrectConsentMixin


class SubjectConsentCorrection(CorrectConsentMixin, BaseUuidModel):

    #     household_member = models.ForeignKey(HouseholdMember)
    #     subject_consent = models.OneToOneField(
    #         SubjectConsent, on_delete=PROTECT)

    subject_identifier = models.CharField(
        max_length=25)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    old_first_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    new_first_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    old_last_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )
    new_last_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    old_initials = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
    )

    new_initials = models.CharField(
        max_length=4,
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

    new_dob = models.DateField(
        verbose_name="New Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    old_gender = models.CharField(
        blank=True,
        null=True,
        max_length=1)

    new_gender = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )

    old_guardian_name = models.CharField(
        max_length=25,
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is '
                           '\'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    new_guardian_name = models.CharField(
        max_length=25,
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
    )

    new_may_store_samples = models.CharField(
        verbose_name="New Sample storage",
        max_length=3,
        blank=True,
        null=True,
    )

    old_is_literate = models.CharField(
        verbose_name="(Old) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
    )

    new_is_literate = models.CharField(
        verbose_name="(New) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
    )

    old_witness_name = models.CharField(
        max_length=25,
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

    new_witness_name = models.CharField(
        max_length=25,
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

#     def __str__(self):
#         return str(self.household_member)
