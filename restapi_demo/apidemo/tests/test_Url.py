from django.urls import reverse,resolve
import pytest
pytestmark = pytest.mark.django_db
class TestUrls:
    def test_index(self):
        path=reverse('index')
        assert resolve(path).view_name=='index'

    def test_signup(self):
        path=reverse('signup')
        assert resolve(path).view_name=='signup'
