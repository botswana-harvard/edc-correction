from django.test import TestCase
from django.test.client import RequestFactory

from ..views import HomeView


class TestHomeView(TestCase):

    def setUp(self):
        self.view = HomeView()
        self.view.request = RequestFactory()

    def test_context(self):
        context = self.view.get_context_data()
        self.assertIn('project_name', context)
