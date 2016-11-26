from django.test import TestCase
from badge.models import BadgeClass, BadgeInstance
from badge.forms import BadgeCreationForm, UserBadgeAssignForm, OneBadgeAssignForm, BadgeSetAvailabilityForm
from django.core.files.uploadedfile import SimpleUploadedFile


# 
# class BadgeClassTestCase(TestCase):
#
#     def test_forms(self):
#         test_image.image = SimpleUploadedFile(
#             name='test_image.jpg',
#             content=open(image_path, 'rb').read(),
#             content_type='image/jpeg'
#         )
#         badge_creation_form_data = {
#             'image':test_image,
#             'name':'test_name',
#             'description':'test_description',
#         }
#         BCForm = BadgeCreationForm(data = badge_creation_form_data)
#         self.assertTrue(form.is_valid())
