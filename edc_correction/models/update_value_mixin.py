from django.apps import apps as django_apps

from edc_constants.constants import YES, NO
from ..exceptions import DataFixError
from edc_base.utils import age, get_utcnow


class UpdateDataValues:

    app_conf = django_apps.get_app_config('edc_correction')
    age_min = app_conf.age_min
    age_is_adult = app_conf.age_is_adult

    def __init__(self, consent_data_fix=None, subject_consent=None, first_name=None, last_name=None,
                 dob=None, initials=None, gender=None, guardian_name=None,
                 may_store_samples=None, is_literate=None, witness_name=None):
        self.consent_data_fix = consent_data_fix
        self.subject_consent = subject_consent
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.initials = initials
        self.gender = gender
        self.guardian_name = guardian_name
        self.may_store_samples = may_store_samples
        self.is_literate = is_literate
        self.witness_name = witness_name

    def update_values(self):
        """Update values of the consent.
        """
        update_fields = ['first_name',
                         'last_name',
                         'dob',
                         'initials',
                         'gender',
                         'guardian_name',
                         'may_store_samples',
                         'is_literate',
                         'witness_name']
        first_name = self.first_name if self.first_name else self.subject_consent.first_name
        last_name = self.last_name if self.last_name else self.subject_consent.last_name

        if self.first_name:
            self.subject_consent.first_name = first_name
        if self.last_name:
            self.subject_consent.last_name = last_name
        self.subject_consent.initials = self.update_initials(
            first_name, last_name)
        self.unverify_consent()
        self.update_dob()
        self.update_witness()
        self.update_guardian_name()
        self.update_is_literate()
        self.subject_consent.user_modified = self.update_user_modified()
        self.subject_consent.save(update_fields=update_fields)

    def update_initials(self, first_name, last_name):
        initials = f'{first_name[0]}{last_name[0]}'
        if self.initials:
            if (self.initials.startswith(initials[0]) and
                    self.initials.endswith(initials[-1])):
                initials = self.initials
            else:
                raise DataFixError(
                    'New initials do not match first and '
                    f'last name. Expected {initials}, Got {self.initials}')
        return initials

    def unverify_consent(self):
        """Unverify a consent.
        """
        self.subject_consent.is_verified = False
        self.subject_consent.is_verified_datetime = None
        self.subject_consent.verified_by = None

    def update_dob(self):
        if self.dob:
            age_in_years = age(self.dob, get_utcnow()).years
            guardian_name = self.guardian_name or self.subject_consent.guardian_name
            if age_in_years < self.age_min:
                raise DataFixError(
                    f'Age is bellow allowed age. Got {age_in_years}. '
                    f'Minimum allowed is {self.age_min}')
            elif (age_in_years >= self.age_min and
                  age_in_years <= self.age_is_adult and not guardian_name):
                raise DataFixError(
                    f'Age is of a minor. Got {age_in_years}. '
                    'Guardian name required')
        if self.dob:
            self.subject_consent.dob = self.dob

    def update_guardian_name(self):
        if self.guardian_name:
            guardian_name = self.guardian_name or self.subject_consent.guardian_name
            dob = self.dob or self.subject_consent.dob
            consent_age_in_years = age(dob, get_utcnow()).years
            if (consent_age_in_years >= self.age_min and
                    consent_age_in_years <= self.age_is_adult and guardian_name):
                self.subject_consent.guardian_name = self.guardian_name
            else:
                raise DataFixError('This is not a minor, no guardian required. '
                                   f'Age is {consent_age_in_years}')

    def update_is_literate(self):
        if self.is_literate:
            witness_name = self.witness_name or self.subject_consent.witness_name
            self.subject_consent.is_literate = self.is_literate
            if self.is_literate == YES:
                self.subject_consent.witness_name = None
            elif self.is_literate == NO and not witness_name:
                raise DataFixError(
                    'Witness name required if is_literate in No')
            else:
                self.subject_consent.witness_name = witness_name

    def update_witness(self):
        if self.witness_name and not self.subject_consent.is_literate:
            self.subject_consent.witness_name = self.witness_name

    def update_user_modified(self):
        user_modified = self.consent_data_fix.user_created
        return user_modified

    class Meta:
        abstract = True
