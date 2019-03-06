#import pytest
from django.test.client import encode_multipart

from .models import Notes
import django
django.setup()
from rest_framework.test import APIRequestFactory
factory = APIRequestFactory()

#pytestmark = pytest.mark.django_db
class Test_Note_Model:
    def test_save(self):
            # add_note = Notes.objects.create(
            #     title="PyTest_checking_note_create",
            #     description="py_description",
            #     is_archived=False,
            #     trash=False
            # )
            # assert add_note.title == "PyTest_checking_note_create"
            # assert add_note.description =="py_description"
            # assert add_note.is_archived == False
            # assert add_note.trash == False
            data= {"title":"PyTest_checking_note_create",
                "description":"py_description",
                "is_archived":False,
                "trash":False}

            content = encode_multipart('BoUnDaRyStRiNg', data)
            content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
            request = factory.put('/addnote/', content, content_type=content_type)

    def test_invalid_data(self):
        data = {"title": "PyTest_checking_note_create",
                "description": None,
                "is_archived": "some_string",
                "trash": False}

        content = encode_multipart('BoUnDaRyStRiNg', data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        request = factory.put('/addnote/', content, content_type=content_type)
