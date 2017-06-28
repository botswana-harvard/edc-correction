# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 09:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django_revision.revision_field
import edc_base.model_fields.hostname_modification_field
import edc_base.model_fields.userfield
import edc_base.model_fields.uuid_auto_field
import edc_base.model_validators.date
import edc_base.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectConsent',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default='magodign.local', help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('subject_identifier', models.CharField(max_length=25)),
                ('report_datetime', models.DateTimeField(null=True, validators=[edc_base.model_validators.date.datetime_not_future], verbose_name='Correction report date ad time')),
                ('first_name', models.CharField(blank=True, max_length=25, null=True)),
                ('new_first_name', models.CharField(blank=True, max_length=25, null=True)),
                ('last_name', models.CharField(blank=True, max_length=25, null=True)),
                ('new_last_name', models.CharField(blank=True, max_length=25, null=True)),
                ('initials', models.CharField(blank=True, max_length=4, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('new_initials', models.CharField(blank=True, max_length=4, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(blank=True, help_text='Format is YYYY-MM-DD', null=True, verbose_name='Old Date of birth')),
                ('new_dob', models.DateField(blank=True, help_text='Format is YYYY-MM-DD', null=True, verbose_name='New Date of birth')),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('new_gender', models.CharField(blank=True, max_length=1, null=True)),
                ('guardian_name', models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[A-Z]{1,50}\\, [A-Z]{1,50}$', "Invalid format. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma")])),
                ('new_guardian_name', models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[A-Z]{1,50}\\, [A-Z]{1,50}$', "Invalid format. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma")])),
                ('may_store_samples', models.CharField(blank=True, max_length=3, null=True, verbose_name='Old Sample storage')),
                ('new_may_store_samples', models.CharField(blank=True, max_length=3, null=True, verbose_name='New Sample storage')),
                ('is_literate', models.CharField(blank=True, max_length=3, null=True, verbose_name='(Old) Is the participant LITERATE?')),
                ('new_is_literate', models.CharField(blank=True, max_length=3, null=True, verbose_name='(New) Is the participant LITERATE?')),
                ('witness_name', models.CharField(blank=True, help_text="Required only if subject is illiterate. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma", max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[A-Z]{1,50}\\, [A-Z]{1,50}$', "Invalid format. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma")], verbose_name="Witness's Last and first name (illiterates only)")),
                ('new_witness_name', models.CharField(blank=True, help_text="Required only if subject is illiterate. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma", max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[A-Z]{1,50}\\, [A-Z]{1,50}$', "Invalid format. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma")], verbose_name="Witness's Last and first name (illiterates only)")),
            ],
        ),
    ]