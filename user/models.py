from django.db import models

# Create your models here.
class User(models.Model):
    mb_id = models.CharField(max_length=50)

    def __str__(self):
        return self.mb_id
    
    class Meta:
        db_table = "user"