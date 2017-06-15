from django.test import TestCase
from ..python_scripts import UpdatePII
from ..models import HouseholdMember
from edc_correction.models import SubjectConsent
from django import forms


class TestUpdatePii(TestCase):

    def test_initial(self):
        UpdatePII(subject_identifier=None)

    def test_create_member_with_sid(self):
        household_member = HouseholdMember.objects.create(
            subject_identifier='765478362486-2')
        UpdatePII(subject_identifier=household_member.subject_identifier)

    def test_change_firstname(self):
        household_member = HouseholdMember.objects.create(
            subject_identifier='65765867535', first_name='Tumie')
        new_first_name = 'Magodi'

        uPII = UpdatePII(
            subject_identifier=household_member.subject_identifier)

        update_name = uPII.update_first_name(new_first_name='Magodi')
        self.assertEqual(update_name, new_first_name)

    def test_change_initials(self):
        household_member = HouseholdMember.objects.create(
            subject_identifier='65765867535', first_name='Tumie')

        uPII = UpdatePII(
            subject_identifier=household_member.subject_identifier)

        update_initials = uPII.update_initials('NOTHANDO', 'MAGODI')
        print('*****', update_initials)
#         self.assertRaises(forms.ValidationError, update_initials)

#     def test_change_last_name(self):
#         household_member = HouseholdMember.objects.create(
#             subject_identifier='65765867535')
#         SubjectConsent.objects.create(
#             household_member=household_member, last_name='JUANITO')
