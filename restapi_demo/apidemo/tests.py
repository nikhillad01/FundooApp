from django.test import TestCase
import pytest
# Create your tests here.
from .models import RestRegistration
pytestmark = pytest.mark.django_db
class TestRegisterModel:
    def test_save(self):
            register = RestRegistration.objects.create(
                username="PyTest",
                password=500,
                confirm_password=500,
                email="nikhillad01@gmail.com"
            )
            assert register.username == "PyTest"
            assert register.password == 500
            assert register.confirm_password == 500
            assert register.email == "nikhillad01@gmail.com"

