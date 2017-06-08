from django.test.testcases import TestCase
from ..python_scripts import UpdatePii
from bcpp_random.models import HouseholdMember, EnrollmentChecklist, SubjectConsent
from django.db.utils import IntegrityError


class TestUpdatePii(TestCase):

    def test_update_hh(self):
        UpdatePii(subject_identifier='765478362486-2')

    def test_with_household_member(self):
        household_member = HouseholdMember.objects.create(subject_identifier='765478362486-2')
        EnrollmentChecklist.objects.create(household_member=household_member)
        UpdatePii(subject_identifier='765478362486-2')

    def test_with_household_member_with_consent(self):
        household_member = HouseholdMember.objects.create(subject_identifier='765478362486-2')
        EnrollmentChecklist.objects.create(household_member=household_member)
        SubjectConsent.objects.create(household_member=household_member, last_name='GABORONE')
        self.assertRaises(
            IntegrityError,
            UpdatePii, subject_identifier='765478362486-2')

    def test_change_lastname(self):
        household_member = HouseholdMember.objects.create(subject_identifier='765478362486-2')
        EnrollmentChecklist.objects.create(household_member=household_member)
        SubjectConsent.objects.create(household_member=household_member, last_name='GABORONE')
        UpdatePii(subject_identifier='765478362486-2', last_name='MOCHUDI')
        obj = SubjectConsent.objects.get(household_member=household_member)
        self.assertEqual(obj.last_name, 'MOCHUDI')




