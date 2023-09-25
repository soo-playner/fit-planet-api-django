from rest_framework import serializers
from user.models import User, Expert
from django.contrib.auth import get_user_model
import re

class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
      model = get_user_model()
      fields = ['mb_email', 'password', 'mb_phone', 'mb_name', 'mb_nickname', 
                'mb_certify', 'mb_services_agree', 'mb_marketing_agree', 'mb_privacy_agree', 'mb_social_type', 'mb_level', 'mb_birth', 'mb_gender']
      extra_kwargs = {
         'password': {'write_only': True}
      }

    def validate_mb_email(self, instance):
      if "admin" in instance:
        raise serializers.ValidationError(detail="사용할 수 없는 메일 계정입니다.")
      return instance
    
    def validate_password(self, instance):
      if len(instance) < 8:
        raise serializers.ValidationError(detail="비밀번호는 8자리 이상 입력해주세요.")
      regex = '^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
      if not re.fullmatch(regex, instance):
        raise serializers.ValidationError(detail="비밀번호 입력 양식을 확인해주세요.")
      return instance

    def create(self, validated_data):
       return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
      model = get_user_model()
      fields = ['id', 'mb_email', 'password', 'mb_phone', 'mb_name', 'mb_nickname', 'mb_social_type', 'mb_level', 'mb_birth', 'mb_gender']
      extra_kwargs = {
         'password': {'write_only': True}
      }

class UserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
      def validate_password(self, instance):
        if len(instance) < 8:
          raise serializers.ValidationError(detail="비밀번호는 8자리 이상 입력해주세요.")
        regex = '^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
        if not re.fullmatch(regex, instance):
          raise serializers.ValidationError(detail="비밀번호 입력 양식을 확인해주세요.")
        return instance

class ExpertSerializer(serializers.ModelSerializer):

  class Meta:
    model = Expert
    fields = ["username", "ep_description", "ep_hours", "ep_education", "ep_license",
              "ep_career", "ep_product", "ep_product_options"]