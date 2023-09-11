# Packages

django
python-dotenv==0.21.0
djangorestframework==3.14.0
pytest==7.4.1
pytest-django-4.5.2

# Commands

django-admin startproject config

from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())

pytest #테스트 파일 모두 실행