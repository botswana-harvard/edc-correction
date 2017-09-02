from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future


class DataUpdateHistory(BaseUuidModel):

    instance_pk = models.CharField(
        max_length=50)

    report_datetime = models.DateTimeField(
        verbose_name="Data update report date and time",
        null=True,
        validators=[
            datetime_not_future],
    )

    new_value = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    old_value = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    model_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    attribute_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
