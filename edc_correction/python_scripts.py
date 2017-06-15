from .models import HouseholdMember
from edc_correction.models import SubjectConsent


class UpdatePII:

    def __init__(self, subject_identifier=None, **fields):

        self.subject_identifier = subject_identifier

    def update_fields(self):
        pass

    def update_first_name(self, new_first_name=None):
        self.new_first_name = new_first_name
        for member in HouseholdMember.objects.filter(subject_identifier=self.subject_identifier):
            member.first_name = self.new_first_name
            member.save()
        return member.first_name

    def update_last_name(self, new_last_name=None):
        self.new_last_name = new_last_name
        for member in SubjectConsent.objects.filter(subject_identifier=self.subject_identifier):
            member.last_name = self.new_last_name
            member.save()
        return member.last_name

    def update_age_in_years(self):
        pass

    def update_initials(self, first_name, last_name):
        for member in HouseholdMember.objects.filter(subject_identifier=self.subject_identifier):
            new_initials = f'{first_name[0]}{last_name[0]}'
            member.initials = new_initials
            member.save()
        return member.initials

    def update_gender(self):
        pass

    def update_is_literate(self):
        pass

    def update_date_of_brith(self):
        pass

    def update_literacy_witness(self):
        pass

    def update_guardian_name(self):
        pass

    def update_enrollment_and_consent(self):
        pass

    def update_user_modified(self):
        user_modified = None
        if not self.id:
            user_modified = self.user_created
        else:
            user_modified = self.user_modified
        return user_modified

    class Meta:
        abstract = True
