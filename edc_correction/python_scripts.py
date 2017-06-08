from django.core.exceptions import ObjectDoesNotExist

from edc_base.utils import get_utcnow
# from edc_registration.models import RegisteredSubject

from .models import HouseholdMember, EnrollmentChecklist, SubjectConsent


class UpdatePii:

    def __init__(self, user_modified=None, initials=None, last_name=None, subject_identifier=None):

        for hm in HouseholdMember.objects.filter(subject_identifier=subject_identifier):
            hm.initials = initials
            hm.user_modified = user_modified
            hm.modified = get_utcnow()
            hm.save()

            for obj in hm.enrollmentchecklist_set.all():
                obj.initials = initials
                obj.user_modified = user_modified
                obj.modified = get_utcnow()
                obj.save()

            for obj in hm.subjectconsent_set.all():
                obj.last_name = last_name
                obj.initials = initials
                obj.user_modified = user_modified
                obj.modified = get_utcnow()
                obj.save()



