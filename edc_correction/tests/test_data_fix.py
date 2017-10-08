from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import MALE

from ..exceptions import DataFixError
from ..models import ConsentDataFix
from ..tests.models import SubjectConsent


class TestDataFix(TestCase):

    def setUp(self):
        options = dict(
            subject_identifier='11111111',
            report_datetime=get_utcnow(),
            first_name='TEST',
            last_name='TEST',
            initials='TT',
            dob=date.today() - relativedelta(years=23),
            gender=MALE,
            may_store_samples='',
            is_literate='Yes',)
        self.subject_consent = SubjectConsent.objects.create(**options)
        self.assertEqual(SubjectConsent.objects.all().count(), 1)

    def test_db_value_equal_old_value(self):
        """Assert no error thrown for comparing db consent value
        against old value entered.
        """
        new_last_name = 'TESTING'
        old_last_name = 'TEST'
        attr_name = 'last_name'
        self.assertEqual(
            getattr(self.subject_consent, attr_name), old_last_name)
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            last_name=new_last_name,
            old_last_name=old_last_name)

    def test_db_value_not_equal_old_value(self):
        """Assert a consent value on the db not equal to the old value provided
        throws an error.
        """
        new_last_name = 'TESTING'
        old_last_name = 'TEST2'
        expected_message = 'Consent db value does not match the old value '\
            'entered for field: last_name value TEST2.'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                last_name=new_last_name,
                old_last_name=old_last_name)

    def test_only_new_value_provided(self):
        """Assert if new value provided without an old value throws an error.
        """
        new_last_name = 'TESTING'
        expected_message = 'Both the old and new value must be provided. '\
            'Got None and TESTING.'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                last_name=new_last_name,)

    def test_only_old_value_provided(self):
        """Assert if old value provided without an new value throws an error.
        """
        old_last_name = 'TEST'
        expected_message = 'Both the old and new value must be provided. '\
            'Got TEST and None.'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                old_last_name=old_last_name)

    def test_old_and_new_value_same(self):
        """Assert if both old and new value are the same an error is thrown.
        """
        new_last_name = 'TEST'
        old_last_name = 'TEST'
        expected_message = 'The old and new value are equal. '\
            f'Got {new_last_name} and {old_last_name}'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                old_last_name=old_last_name,
                last_name=new_last_name)

    def test_validate_value_against_consent(self):
        """Assert of old value provided is the same as the db value.
        """
        new_last_name = 'TESTING'
        old_last_name = 'TEST'
        attr_name = 'last_name'
        consent_data_fix = ConsentDataFix.objects.create(
            subject_identifier='11111111',
            last_name=new_last_name,
            old_last_name=old_last_name)
        self.assertTrue(
            consent_data_fix.validate_value_against_consent(
                subject_consent=self.subject_consent,
                value=old_last_name, attr_name=attr_name))
