from rest_framework import serializers
from expert.models import Expert

class ExpertSerializer(serializers.ModelSerializer):

  class Meta:
    model = Expert
    fields = ["username", "ep_description", "ep_hours", "ep_education", "ep_license",
              "ep_career", "ep_product", "ep_product_options"]