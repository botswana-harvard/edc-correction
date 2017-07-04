from datetime import timezone
from edc_base.model_validators.date import datetime_not_future
from edc_base.utils import get_utcnow

from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.test import TestCase

from .forms import SubjectConsentCorrectionForm


class TestModelsMixin:

    subject_identifier = models.CharField(
        max_length=25)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    first_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    initials = models.CharField(
        max_length=4,
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        blank=True,
    )

    dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    gender = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )


class HouseholdMember(TestModelsMixin, models.Model):

    pass


class EnrollmentChecklist(TestModelsMixin, models.Model):

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)


class SubjectConsent(models.Model):

    enrollment_checklist = models.ForeignKey(
        EnrollmentChecklist, on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        max_length=25)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    first_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    initials = models.CharField(
        max_length=4,
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        blank=True,
    )

    dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
    )

    gender = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )

    guardian_name = models.CharField(
        max_length=25,
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$',
                           'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                           'All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    may_store_samples = models.CharField(
        verbose_name="Sample storage",
        max_length=3,
        blank=True,
        null=True,
    )

    is_literate = models.CharField(
        verbose_name="Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
    )

    witness_name = models.CharField(
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


class TestCorrectConsent(TestCase):

    def setUp(self):
        self.hhm = HouseholdMember()
        self.hhm.first_name = 'Magodi'
        self.hhm.initials = 'MGD'
        self.hhm.subject_identifier = '1234'

        self.ec = EnrollmentChecklist()
        self.ec.subject_identifier = '1234'
        self.ec.first_name = 'Magodi'
        self.ec.initials = 'MGD'
        self.ec.household_member = self.hhm

        self.subject_consent = SubjectConsent()
        self.subject_consent.subject_identifier = '1234'
        self.subject_consent.enrollment_checklist = self.ec
        self.subject_consent.first_name = 'Magodi'
        self.subject_consent.initials = 'MGD'

    def test_change_firstname(self):
        cleaned_data = {'report_datetime': get_utcnow(),
                        'old_first_name': 'Magodi',
                        'new_first_name': 'Tumie'}
        form = SubjectConsentCorrectionForm(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.save)

# #     def test_initial(self):
# #         CorrectConsent(subject_identifier=None)
#
# #     def test_create_member_with_sid(self):
# #         household_member = HouseholdMember.objects.create(
# #             subject_identifier='765478362486-2')
# # #         CorrectConsent(subject_identifier=household_member.subject_identifier)
#
#     def test_change_firstname(self):
#         household_member = HouseholdMember.objects.create(
#             subject_identifier='65765867535', first_name='Tumie')
#         new_first_name = 'Magodi'
#
#         updated_name = CorrectConsent.correct_pii_in_all_survey(
#             self, subject_identifier=household_member.subject_identifier,
#             new_first_name=new_first_name)
#
#         self.assertEqual(new_first_name, updated_name)
#
# #     def test_change_initials(self):
# #         household_member = HouseholdMember.objects.create(
# #             subject_identifier='65765867535', first_name='Tumie')
# #
# #         uPII = CorrectConsent(
# #             subject_identifier=household_member.subject_identifier)
# #
# #         update_initials = uPII.update_initials('NOTHANDO', 'MAGODI')
# #         print('*****', update_initials)
# #         self.assertRaises(forms.ValidationError, update_initials)
# #
# #     def test_change_last_name(self):
# #         household_member = HouseholdMember.objects.create(
# #             subject_identifier='65765867535')
# #         SubjectConsent.objects.create(
# #             household_member=household_member, last_name='JUANITO')
