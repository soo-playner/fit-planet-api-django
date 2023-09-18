from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    # username = serializers.EmailField(source="user.username", required=True)
    # mb_phone = serializers.CharField(source="user.mb_phone", required=True)
    # mb_name = serializers.CharField(source="user.mb_name", required=True)
    # mb_nickname = serializers.CharField(source="user.mb_nickname", required=True)
    # mb_certify = serializers.BooleanField(source="user.mb_certify", required=True)
    # mb_services_agree = serializers.BooleanField(source="user.mb_services_agree", required=True)
    # mb_marketing_agree = serializers.BooleanField(source="user.mb_marketing_agree", required=True)
    # mb_privacy_agree = serializers.BooleanField(source="user.mb_privacy_agree", required=True)
    # mb_social_type = serializers.CharField(source="user.mb_social_type", required=True)
    # mb_level = serializers.IntegerField(source="user.mb_level", required=True)

    def create(self, validated_data):
        password = validated_data['password']
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    class Meta:
      model = get_user_model()
      fields = ["username", "password", "mb_phone", "mb_name", "mb_nickname", "mb_certify", 
                "mb_services_agree", "mb_marketing_agree", "mb_privacy_agree",
                "mb_social_type", "mb_level", "mb_birth", "mb_gender", "mb_profile_image", 
              ]
