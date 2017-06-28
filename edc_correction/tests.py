from django.test import TestCase
from .models import SubjectConsent
from .correct_consent import CorrectConsent


class TestCorrectConsent(TestCase):

    def test_initial(self):
        CorrectConsent.updated_field_validations(self)

    def test_change_first_name_not_none(self):
        SubjectConsent.first_name = 'MAGODI'
        SubjectConsent.new_first_name = 'MOTHANDO'
        CorrectConsent.change_first_name(self)
        self.assertEqual(SubjectConsent.new_first_name,
                         SubjectConsent.first_name)

    def test_change_first_name_is_none(self):
        SubjectConsent.first_name = 'MAGODI'
        SubjectConsent.new_first_name = None
        CorrectConsent.change_first_name(self)
        self.assertEqual(SubjectConsent.first_name,
                         SubjectConsent.first_name)

    def test_change_last_name_not_none(self):
        SubjectConsent.last_name = 'MAMSON'
        SubjectConsent.new_last_name = 'MANG'
        CorrectConsent.change_last_name(self)
        self.assertEqual(SubjectConsent.new_last_name,
                         SubjectConsent.last_name)

    def test_change_last_name_is_none(self):
        SubjectConsent.last_name = 'MADEIRA'
        SubjectConsent.new_last_name = None
        CorrectConsent.change_last_name(self)
        self.assertEqual(SubjectConsent.last_name,
                         SubjectConsent.last_name)
