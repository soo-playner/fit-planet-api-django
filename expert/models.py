from django.db import models

# Create your models here.
class Expert(models.Model):

    username = models.EmailField(max_length=255, unique=True)
    ep_description = models.TextField()
    ep_hours = models.TextField()
    ep_education = models.TextField()
    ep_license = models.TextField()
    ep_career = models.TextField()
    ep_product = models.JSONField(default=dict)
    ep_product_options = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "expert"