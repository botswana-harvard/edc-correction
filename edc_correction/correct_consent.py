from .models import SubjectConsent
from django import forms


class CorrectConsent:

    def __init__(self, subject_identifier=None, initials='MM'):
        self.subject_identifier = subject_identifier
        self.initials = initials
#         self.subject_consent = SubjectConsent.objects.all()
#         self.member_model = SubjectConsent.objects.filter(subject_identifier)

    def compare_current_field_value_new_field_value(self):
        pass

    def change_first_name(self):
        if SubjectConsent.new_first_name:
            SubjectConsent.first_name = SubjectConsent.new_first_name
            if f'(first_name[0], last_name[0])' == SubjectConsent.initials:
                print(SubjectConsent.initials)

            print('Initials do not tally, do you want t update Initalls also')

    def change_last_name(self):
        if SubjectConsent.new_last_name:
            SubjectConsent.last_name = SubjectConsent.new_last_name

    def updated_field_validations(self):

        fields = [
            f.name for f in SubjectConsent._meta.get_fields()
        ]
#         print(fields)
#         for field in fields:
#             print(field, getattr(SubjectConsent, field))

        #             field_value = getattr(HouseholdMember, field)
        #             if field1 == 'first_name':
        #                 print('first name is', field_value)
        #                 if field_value:
        #                     pass
        #             elif field1 == 'initials':
        #                 print('initials', field_value)
        #             elif field1 == 'gender':
        #                 print('gender is', field_value)
        #             elif field1 == 'age_in_years':
        #                 print('age_in_years is', field_value)
        #             elif field1 == 'user_modified':
        #                 print('user_modified is', field_value)
        #             else:
        #                 print('Field Does Not Exist')
#         return fields

    def update_enrollment_checklist_and_consent(self):
        pass
