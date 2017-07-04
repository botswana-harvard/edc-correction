from datetime import timezone
from edc_base.model_validators.date import datetime_not_future

from dateutil.relativedelta import relativedelta
from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.test import TestCase

from .models import SubjectConsentCorrection, CorrectConsentMixin


class SubjectConsent:
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
        self.subject_consent = SubjectConsent()
        self.subject_consent.first_name = 'Magodi'


#     def mommy(self):
#
#         subject_consent = SubjectConsent.objects.create(
#             subject_identifier='subject_identifier',
#             first_name='Amanda',
#             last_name='India',
#             initials='AI',
#             dob='new_dob',
#             is_literate='new_is_literate',
#             gurdian_name='new_guardian_name',
#             gender='new_gender',
#             may_store_samples='new_may_store_samples'
#         )
#
#         household_member = HouseholdMember.objects.create(
#             subject_identifier='subject_identifier',
#             first_name='Amanda',
#             initials='AI',
#             age_in_years=timezone.now() - relativedelta(years=subject_consent.dob)
#         )
#
#         enrollment_checklist = EnrollmentChecklist.objects.create(
#             household_member=household_member,
#             first_name=household_member.first_name,
#             initials=household_member.initials,
#             dob=subject_consent.dob,
#             gender=subject_consent.gender,
#             is_literate=subject_consent.is_literate,
#         )
#
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
