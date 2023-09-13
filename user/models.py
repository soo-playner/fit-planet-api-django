from django.db import models
from django.contrib.auth.models import AbstractUser
from config.base.model import BaseModel
# Create your models here.
class User(AbstractUser,BaseModel):
    # mb_password = models.CharField(max_length=255)



    def __str__(self):
        return self.mb_id
    class Meta:
        db_table = "user"