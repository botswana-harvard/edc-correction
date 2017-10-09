from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES, NO

from ..exceptions import DataFixError
from ..models import ConsentDataFix
from ..tests.models import SubjectConsent


class TestUpdateValuesMixin(TestCase):

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
            is_literate='Yes',
            user_modified='ttest')
        self.subject_consent = SubjectConsent.objects.create(**options)
        self.assertEqual(SubjectConsent.objects.all().count(), 1)

    def test_first_name(self):
        """Assert if initials are updated on a consent.
        """
        new_first_name = 'DESTING'
        old_first_name = 'TEST'
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            first_name=new_first_name,
            old_first_name=old_first_name)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.first_name, new_first_name)
        self.assertEqual(subject_consent.initials, 'DT')

    def test_last_name(self):
        """Assert if initials are updated on a consent.
        """
        new_last_name = 'DESTING'
        old_last_name = 'TEST'
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            last_name=new_last_name,
            old_last_name=old_last_name)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.last_name, new_last_name)
        self.assertEqual(subject_consent.initials, 'TD')

    def unverify_consent(self):
        """Assert that a consent is unverified.
        """
        new_last_name = 'DESTING'
        old_last_name = 'TEST'
        self.subject_consent.is_verified = True
        self.subject_consent.is_verified_datetime = get_utcnow()
        self.subject_consent.verified_by = 'ckgathi'
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertTrue(subject_consent.is_verified)
        self.assertEqual(self.subject_consent.verified_by, 'ckgathi')
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            last_name=new_last_name,
            old_last_name=old_last_name)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertFalse(subject_consent.is_verified)
        self.assertIsNone(self.subject_consent.verified_by)

    def test_update_initials(self):
        """Assert if initials are updated on a consent.
        """
        new_last_name = 'DESTING'
        old_last_name = 'TEST'
        old_initials = 'TT'
        new_initials = 'TD'
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            last_name=new_last_name,
            old_last_name=old_last_name,
            initials=new_initials,
            old_initials=old_initials)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.initials, new_initials)

    def test_update_initials2(self):
        """Assert that an error is thrown for wrong initials.
        """
        new_last_name = 'DESTING'
        old_last_name = 'TEST'
        old_initials = 'TT'
        new_initials = 'TK'
        expected_message = 'New initials do not match first and last name. '\
            'Expected TD, Got TK'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                last_name=new_last_name,
                old_last_name=old_last_name,
                initials=new_initials,
                old_initials=old_initials)

    def test_update_dob(self):
        """Assert if dob gets updated on a consent.
        """
        new_dob = date.today() - relativedelta(years=25)
        old_dob = date.today() - relativedelta(years=23)
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            dob=new_dob,
            old_dob=old_dob,)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.dob, new_dob)

    def test_update_dob_under_age(self):
        """Assert if dob is changed to a minor an error is thrown.
        """
        new_dob = date.today() - relativedelta(years=14)
        old_dob = date.today() - relativedelta(years=23)
        expected_message = 'Age is bellow allowed age. Got 14. Minimum allowed is 16'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                dob=new_dob,
                old_dob=old_dob)

    def test_update_dob_minor(self):
        """Assert if dob is changed to a minor an error is thrown if no guardian.
        """
        new_dob = date.today() - relativedelta(years=17)
        old_dob = date.today() - relativedelta(years=23)
        expected_message = 'Age is of a minor. Got 17. Guardian name required'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                dob=new_dob,
                old_dob=old_dob)

    def test_update_dob_minor_with_guardian(self):
        """Assert if dob is changed to a minor with guardian provided.
        """
        new_dob = date.today() - relativedelta(years=17)
        old_dob = date.today() - relativedelta(years=23)
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            guardian_name='TEST,TEST',
            dob=new_dob,
            old_dob=old_dob,)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.dob, new_dob)

    def test_update_guardian_name(self):
        """Assert if guardian name is updated for a minor.
        """
        new_dob = date.today() - relativedelta(years=17)
        old_dob = date.today() - relativedelta(years=23)
        guardian_name = 'TEST,TEST'
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            guardian_name=guardian_name,
            dob=new_dob,
            old_dob=old_dob)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.dob, new_dob)
        self.assertEqual(subject_consent.guardian_name, guardian_name)

    def test_update_guardian_name_not_minor(self):
        """Assert that an error is thrown if guardian name is updated
        if not a minor.
        """
        expected_message = 'This is not a minor, no guardian required. '\
            'Age is 23'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                guardian_name='TEST,TEST')

    def test_update_is_literate(self):
        """Assert if is_literate is yes witness_name is set to N?A.
        """
        is_literate = YES
        old_is_literate = NO
        SubjectConsent.objects.filter(
            id=self.subject_consent.id).update(
                **{'is_literate': NO, 'witness_name': 'TEST,TEST'})
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            old_is_literate=old_is_literate,
            is_literate=is_literate)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.is_literate, is_literate)
        self.assertIsNone(subject_consent.witness_name)

    def test_update_is_not_literate(self):
        """Assert if is_literate is no witness_name is required.
        """
        is_literate = NO
        old_is_literate = YES
        expected_message = 'Witness name required if is_literate in No'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                old_is_literate=old_is_literate,
                is_literate=is_literate)

    def test_update_witness(self):
        """Assert if witness is provided with is_literate as no witness name '
        'is updated.
        """
        witness_name = 'TEST2,TEST2'
        is_literate = NO
        old_is_literate = YES
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            witness_name=witness_name,
            old_is_literate=old_is_literate,
            is_literate=is_literate)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.witness_name, witness_name)
        self.assertEqual(subject_consent.is_literate, is_literate)

    def test_update_witness2(self):
        """Assert if witness is provided with is_literate as no witness name '
        'is updated.
        """
        witness_name = 'TEST2,TEST2'
        expected_message = 'Witness name only required if is_literate in No.'
        with self.assertRaisesMessage(DataFixError, expected_message):
            ConsentDataFix.objects.create(
                subject_identifier='11111111',
                witness_name=witness_name)

    def test_update_is_not_literate2(self):
        """Assert if is_literate is no witness_name is required.
        """
        is_literate = NO
        old_is_literate = YES
        witness_name = 'TEST,TEST'
        ConsentDataFix.objects.create(
            subject_identifier='11111111',
            old_is_literate=old_is_literate,
            is_literate=is_literate,
            witness_name=witness_name)
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.is_literate, is_literate)
        self.assertEqual(subject_consent.witness_name, witness_name)

    def test_update_user_modified(self):
        """Assert if is_literate is no witness_name is required.
        """
        new_last_name = 'DESTING'
        old_last_name = 'TEST'
        consent_data_fix = ConsentDataFix.objects.create(
            subject_identifier='11111111',
            last_name=new_last_name,
            old_last_name=old_last_name,
            user_created='dtest')
        subject_consent = SubjectConsent.objects.get(
            id=self.subject_consent.id)
        self.assertEqual(subject_consent.last_name, new_last_name)
        self.assertEqual(
            subject_consent.user_modified, consent_data_fix.user_created)
