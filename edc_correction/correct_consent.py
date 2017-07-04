from edc_base.utils import get_utcnow

from edc_correction.models.models import SubjectConsent, HouseholdMember


class CorrectConsent:

    def __init__(self, subject_identifier=None):
        self.subject_identifier = subject_identifier

    def correct_member_enrollement(self, subject_identifier=None, new_user_modified=None,
                                   new_initials=None, new_first_name=None, new_gender=None,
                                   new_dob=None, new_is_literate=None):

        for hm in HouseholdMember.objects.filter(subject_identifier=subject_identifier):
            hm.initials = new_initials
            hm.first_name = new_first_name,
            hm.gender = new_gender
            hm.user_modified = new_user_modified
            hm.modified = get_utcnow()
            hm.save()

            for obj in hm.enrollmentchecklist_set.all():
                obj.initials = new_initials
                obj.gender = new_gender
                obj.is_literate = new_is_literate
                obj.dob = new_dob
                obj.user_modified = new_user_modified
                obj.modified = get_utcnow
                obj.save()

            return hm.first_name, hm.gender, hm.initials, hm.modified, hm.user_modified

    def update_consent(self, subject_identifier=None, new_user_modified=None,
                       new_initials=None, new_first_name=None,
                       new_last_name=None, new_gender=None,
                       new_dob=None, new_guardian_name=None):

        for sc in SubjectConsent.objects.filter(subject_identifier=subject_identifier):
            sc.first_name = new_first_name
            sc.last_name = new_last_name
            sc.initials = new_initials
            sc.gender = new_gender
            sc.dob = new_dob
            sc.guardian_name = new_guardian_name
            sc.user_modified = new_user_modified
            sc.modified = get_utcnow()
            sc.save()

            return (sc.dob, sc.first_name, sc.gender, sc.guardian_name,
                    sc.initials, sc.last_name, sc.modified, sc.user_modified)
