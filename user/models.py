from django.db import models
from django.contrib.auth.models import AbstractUser
from config.base.model import BaseModel
# Create your models here.
class User(AbstractUser,BaseModel):
    
    first_name = None
    last_name = None
    email = None

    username = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    mb_phone = models.CharField(max_length=20)
    mb_name = models.CharField(max_length=50)
    mb_nickname = models.CharField(max_length=50)
    mb_certify = models.BooleanField(default=False)
    mb_services_agree = models.BooleanField(default=False)
    mb_marketing_agree = models.BooleanField(default=False)
    mb_privacy_agree = models.BooleanField(default=False)
    mb_social_type = models.CharField(max_length=1)
    mb_level = models.SmallIntegerField(default=1)
    mb_birth = models.CharField(max_length=8, blank=True)
    mb_gender = models.CharField(max_length=1, blank=True)
    mb_profile_image = models.FileField(upload_to='', blank=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "user"