from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class DataFixValidationMixin:

    @property
    def subject_consents(self):
        """Return subject consents."""
        consent_label_lower = django_apps.get_app_config(
            'edc_correction').consent_model
        consent_model_cls = django_apps.get_model(consent_label_lower)
        return consent_model_cls.objects.filter(
            subject_identifier=self.subject_identifier)

    def validate_value_against_consent(
            self, subject_consent=None, value=None, attr_name=None):
        """Return True if the old value provided is the same a the value
        in the database.
        """
        if getattr(subject_consent, attr_name) == value:
            return True
        return False

    def compare_old_fields_to_db_values(
            self, subject_consent=None, instance=None, exception_cls=None):
        """Raises an exception if an 'old_" field does not match the value
        on the corresponding subject_consent field value."""
        exception_cls = exception_cls or ValidationError
        instance = instance or self
        ignore_fields = ['guardian_name', 'witness_name']
        for field in instance._meta.fields:
            if field.name.startswith('old_'):
                old_value = getattr(instance, field.name)
                new_field_name = field.name.split('old_')[1]
                new_value = getattr(instance, new_field_name)
                if old_value and new_value and old_value == new_value:
                    raise exception_cls(
                        'The old and new value are equal. '
                        f'Got {old_value} and {new_value}')
                if new_field_name not in ignore_fields:
                    if ((not old_value and new_value) or
                            (old_value and not new_value)):
                        raise exception_cls(
                            'Both the old and new value must be provided. '
                            f'Got {old_value} and {new_value}.')
                    elif old_value and new_value:
                        if not self.validate_value_against_consent(
                                subject_consent=subject_consent,
                                value=old_value, attr_name=new_field_name):
                            raise exception_cls(
                                "Consent db value does not match the old value "
                                f"entered for field: {new_field_name} value {old_value}.")

    class Meta:
        abstract = True
