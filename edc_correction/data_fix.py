from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .models import DataUpdateHistory


class DataFixError(Exception):
    pass


class DataFix:

    def __init__(self, pk=None, attr_name=None, new_value=None, old_value=None, model=None):
        self.new_value = new_value
        self.old_value = old_value
        self.attr_name = attr_name
        self.model = model
        self.pk = pk

    @property
    def model_cls(self):
        return django_apps.get_model(self.model)

    def update_value(self):
        """Update an object instance."""
        try:
            self.model_cls.objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            raise DataFixError(
                f'The object of pk {self.pk} does not exist.')
        else:
            self.model_cls.objects.filter(
                pk=self.pk).update(**self.update_options)

    @property
    def update_options(self):
        return {self.attr_name: self.new_value}

    def valid_old_value(self):
        """Validate if the old value is correct."""
        try:
            obj = self.model_cls.objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            raise DataFixError(
                f'obj of pk {self.pk} does not exist.')
        else:
            if getattr(obj, self.attr_name) == self.old_value:
                return True
            else:
                return False

    def data_update(self):
        """Update instance value and creates a history.
        """
        if self.valid_old_value():
            self.update_value()
            DataUpdateHistory.objects.create(
                instance_pk=self.pk, new_value=self.new_value,
                old_value=self.old_value, model=self.model)
