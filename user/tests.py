from rest_framework.test import APITestCase
from rest_framework.views import status

from .models import *

# Create your tests here.
class UserCreateTestCase(APITestCase):
  def setUp(self):
    self.url = '/v1/user/create/'
    self.data = {
      "username": "sample@sample.com",
      "password": "1234",
      "is_superuser": 1,
      "is_staff": 1,
      "is_active": 1,
      "date_joined": "2023-09-18",
      "mb_phone": "01012345678",
      "mb_name": "테스트",
      "mb_nickname": "sample",
      "mb_certify": True,
      "mb_services_agree": True,
      "mb_marketing_agree": False,
      "mb_privacy_agree": False,
      "mb_social_type": "d",
      "mb_level": 1,
      "mb_birth": "",
      "mb_gender": ""
    }

  def test_user_create(self):
    response = self.client.post(self.url, data=self.data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)