from django.core.exceptions import ValidationError

from member.models import HouseholdMember


class CorrectConsentMixin:

    def save(self, *args, **kwargs):
        self.compare_new_fields_with_exisiting()
        self.update_household_member_and_enrollment_checklist()
        super().save(*args, **kwargs)

    def compare_new_fields_with_exisiting(self, instance=None, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        instance = instance or self

        new_fields = [
            f for f in instance._meta.fields if f.name.startswith('new_')]

        old_fields = [
            f for f in instance._meta.fields if f.name.startswith('old_')]

        for old_field, new_field in zip(old_fields, new_fields):
            old_value = getattr(instance, old_field)
            new_value = getattr(instance, new_field)
            if (new_value and not old_value) or (not new_value and old_value):
                raise exception_cls(
                    'Both the old and new value must '
                    f'be provided. Got \'{old_value}\' and \'{new_value}\'.'
                    f'See {old_field} and {new_field}.')
            elif old_value and new_value and old_value == new_value:
                raise exception_cls(
                    f'The old and new value are equal. Got \'{old_value}\' and'
                    f' \'{new_value}\'.See {old_field} and {new_field}.')
            elif old_value and new_value:
                subject_consent_value = getattr(instance.subject_consent,
                                                old_field.name.split('old_')[1])
                if old_value != subject_consent_value:
                    raise exception_cls(
                        f"Consent '{old_field.name.split('old_')[1]}' does"
                        f"not match '{old_field.name}'."
                        f" Expected '{subject_consent_value}'."
                        f"Got '{old_value}'.")

    def update_household_member_and_enrollment_checklist(self):
        household_member_qs = HouseholdMember.objects.filter(
            subject_identifier=self.subject_identifier)
        for hm in household_member_qs:
            self.update_first_name(hm)

    def update_first_name(self, household_member):
        if self.new_first_name:
            household_member.first_name = self.new_first_name
            if not household_member.initials.startswith(self.new_first_name[0]):
                household_member.initials = (
                    self.new_first_name[0] + household_member.initials[1:])
            if household_member.enrollment_checklist.subject_consent:
                household_member.enrollment_checklist.subject_consent.first_name = (
                    self.new_first_name)

    def update_witness(self, household_member):
        if self.new_witness_name and household_member.enrollment_checklist.subject_consent:
            household_member.enrollment_checklist.subject_consent.witness_name = self.new_witness_name

    def update_gender(self, household_member):
        if self.new_gender:
            household_member.gender = self.new_gender
            if household_member.enrollment_checklist:
                household_member.enrollment_checklist.gender = self.new_gender
                household_member.enrollment_checklist.user_modified = self.update_user_modified()
            household_member.enrollment_checklist.subject_consent.gender = self.new_gender

    def update_initials(self, first_name, last_name):
        initials = '{}{}'.format(first_name[0], last_name[0])
        if self.new_initials:
            if (self.new_initials.startswith(initials[0]) and
                    self.new_initials.endswith(initials[-1])):
                initials = self.new_initials
            else:
                raise ValidationError(
                    'New initials do not match first and '
                    'last name. Expected {}, Got {}'.format(
                        initials, self.new_initials))
        return initials
