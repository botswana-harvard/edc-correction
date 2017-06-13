from django.test import TestCase
from ..python_scripts import UpdatePII
from ..models import HouseholdMember


class TestUpdatePii(TestCase):

    def test_change_firstname(self):
        household_member = HouseholdMember.objects.create(
            subject_identifier='65765867535', first_name='Tumie')
        updated_name = UpdatePII.update_first_name(
            self, subject_identifier=household_member.subject_identifier,
            new_first_name='Magodi')
        self.assertEqual(updated_name, self.new_first_name)
