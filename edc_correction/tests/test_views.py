# from django.apps import apps as django_apps
from django.test import TestCase
from django.test.client import RequestFactory
# from django.views.generic.base import ContextMixin
# from django.test.utils import override_settings
from edc_correction.views import HomeView


class TestHomeView(TestCase):

    def setUp(self):
        self.view = HomeView()
        self.view.request = RequestFactory()

    def test_context(self):
        context = self.view.get_context_data()
        self.assertIn('project_name', context)
