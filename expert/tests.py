from rest_framework.test import APITestCase
from rest_framework.views import status

from .models import *

# Create your tests here.
class UserCreateTestCase(APITestCase):
  def setUp(self):
    self.url = '/v1/expert/create/'
    self.data = {
        "username": "sample8@naver.com",
        "ep_description": "안녕하세요 자기소개입니다",
        "ep_hours": "매일 오전 11시 ~ 오후 7시",
        "ep_education": "한국체육대학교 학사",
        "ep_license": "물리치료사 1급",
        "ep_career": "국가대표 팀닥터 출신",
        "ep_product": {
            "product1": "재활치료 1회권",
            "product2": "재활치료 5회권",
            "product3": "재활치료 10회권"
        },
        "ep_product_options": {
            "option1": "운동복",
            "option2": "락커 이용권"
        }
    }

  def test_user_create(self):
    response = self.client.post(self.url, data=self.data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)