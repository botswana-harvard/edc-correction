from django.test import TestCase

from ..data_fix import DataFix, DataFixError
from ..models import DataUpdateHistory
from ..tests.models import DataFixTestModel


class TestDataFix(TestCase):

    def test_update_value(self):
        """Assert if value of obj is updated.
        """
        obj = DataFixTestModel.objects.create(
            field1='test value')
        old_value = 'test value'
        new_value = 'test new value'
        attr_name = 'field1'
        data_fix = DataFix(
            pk=obj.pk, attr_name=attr_name, new_value=new_value,
            old_value=old_value, model='edc_correction.datafixtestmodel')
        data_fix.update_value()
        obj = DataFixTestModel.objects.get(pk=obj.pk)
        self.assertEqual(getattr(obj, attr_name), new_value)

    def test_update_value1(self):
        """Assert if an error is raised if an object with a given pk
        does not exist.
        """
        pk = '1'
        old_value = 'test value'
        new_value = 'test new value'
        attr_name = 'field1'
        data_fix = DataFix(
            pk=pk, attr_name=attr_name, new_value=new_value,
            old_value=old_value, model='edc_correction.datafixtestmodel')
        self.assertRaises(DataFixError, data_fix.update_value)

    def test_valid_old_value(self):
        """Assert if valid_old_value returns True if old value is not the same
        as the old value in the db.
        """
        obj = DataFixTestModel.objects.create(
            field1='test value')
        old_value = 'test value'
        data_fix = DataFix(
            pk=obj.pk, attr_name='field1',
            old_value=old_value, model='edc_correction.datafixtestmodel')
        self.assertTrue(data_fix.valid_old_value())

    def test_wrong_valid_old_value(self):
        """Assert if valid_old_value returns True if old value is not the same
        as the old value in the db.
        """
        obj = DataFixTestModel.objects.create(
            field1='test value')
        old_value = 'test value 1'
        data_fix = DataFix(
            pk=obj.pk, attr_name='field1',
            old_value=old_value, model='edc_correction.datafixtestmodel')
        self.assertFalse(data_fix.valid_old_value())

    def test_valid_old_value_no_obj(self):
        """Assert if valid_old_value returns True if old value is not the same
        as the old value in the db.
        """
        pk = '1'
        old_value = 'test value 1'
        data_fix = DataFix(
            pk=pk, attr_name='field1',
            old_value=old_value,
            model='edc_correction.datafixtestmodel')
        self.assertRaises(DataFixError, data_fix.valid_old_value)

    def test_data_update(self):
        """Assert if a history is created for an updated model instance value.
        """
        obj = DataFixTestModel.objects.create(
            field1='test value')
        old_value = 'test value'
        data_fix = DataFix(
            pk=obj.pk, attr_name='field1',
            old_value=old_value, model='edc_correction.datafixtestmodel')
        self.assertEqual(DataUpdateHistory.objects.all().count(), 0)
        data_fix.data_update()
        self.assertEqual(DataUpdateHistory.objects.all().count(), 1)
        self.assertEqual(
            DataUpdateHistory.objects.filter(instance_pk=obj.pk).count(), 1)
