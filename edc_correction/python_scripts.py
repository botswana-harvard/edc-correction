from .models import HouseholdMember


class UpdatePII:

    def update_first_name(self, subject_identifier=None, new_first_name=None):
        self.subject_identifier = subject_identifier
        self.new_first_name = new_first_name
        for member in HouseholdMember.objects.filter(subject_identifier=self.subject_identifier):
            member.first_name = self.new_first_name
            member.save()
        return member.first_name

    def update_last_name(self):
        pass

    def update_age_in_years(self):
        pass

    def update_initials(self):
        pass

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

    def update_user_modified(self):
        pass
