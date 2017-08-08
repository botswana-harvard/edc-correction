from django.db import models
from edc_base.utils import get_utcnow


class DataFixTestModel(models.Model):

    report_datetime = models.DateTimeField(default=get_utcnow)

    field1 = models.CharField(
        max_length=25, null=True)
