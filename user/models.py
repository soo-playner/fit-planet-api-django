from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from config.base.model import BaseModel

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, mb_email, password, **extra_fields):
        if not mb_email:
            raise ValueError('이메일은 필수입력입니다.')
        user = self.model(mb_email=mb_email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, mb_email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('mb_name', '최고관리자')
        extra_fields.setdefault('mb_nickname', '최고관리자')
        extra_fields.setdefault('mb_level', 10)
        user = self.model(mb_email=mb_email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractBaseUser, BaseModel):

    mb_email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    mb_phone = models.CharField(max_length=20)
    mb_name = models.CharField(max_length=10)
    mb_nickname = models.CharField(max_length=10, unique=True)
    mb_certify = models.BooleanField(default=False)
    mb_services_agree = models.BooleanField(default=False)
    mb_marketing_agree = models.BooleanField(default=False)
    mb_privacy_agree = models.BooleanField(default=False)
    mb_social_type = models.CharField(max_length=1)
    mb_level = models.SmallIntegerField(default=1)
    mb_birth = models.CharField(max_length=8, blank=True)
    mb_gender = models.CharField(max_length=1, blank=True)
    mb_profile_image = models.FileField(upload_to='', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'mb_email'

    def __str__(self):
        return self.mb_email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "user"

class Expert(models.Model):

    mb_no = models.BigIntegerField(unique=True)
    mb_email = models.EmailField(max_length=255, unique=True)
    ep_description = models.TextField()
    ep_hours = models.TextField()
    ep_education = models.TextField()
    ep_license = models.TextField()
    ep_career = models.TextField()
    ep_product = models.TextField()
    ep_product_options = models.TextField()

    def __str__(self):
        return self.mb_email
    class Meta:
        db_table = "expert"