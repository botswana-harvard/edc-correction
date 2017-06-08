from django.db import models
from edc_base.model_mixins import BaseUuidModel


class HouseholdMember(BaseUuidModel):
    subject_identifier = models.CharField(
        max_length=25)


class EnrollmentChecklist(BaseUuidModel):

    household_member = models.ForeignKey(HouseholdMember)


class SubjectConsent(BaseUuidModel):

    last_name = models.CharField(
        max_length=25)

    household_member = models.ForeignKey(HouseholdMember)
