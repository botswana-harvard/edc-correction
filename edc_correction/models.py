from django.db import models
from edc_base.model_mixins import BaseUuidModel
from django.core.validators import RegexValidator


class HouseholdMember(BaseUuidModel):
    subject_identifier = models.CharField(
        max_length=25)

    first_name = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    new_first_name = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    initials = models.CharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        max_length=3,
        blank=True)

    new_initials = models.CharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        max_length=3,
        blank=True)


class EnrollmentChecklist(BaseUuidModel):

    household_member = models.ForeignKey(HouseholdMember)


class SubjectConsent(BaseUuidModel):

    last_name = models.CharField(
        max_length=25)

    new_last_name = models.CharField(
        max_length=25)

    household_member = models.ForeignKey(HouseholdMember)
