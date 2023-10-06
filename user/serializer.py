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

class UserEmailDupSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['mb_email']
  
  def validate_mb_email(self, instance):
    if "admin" in instance:
      raise serializers.ValidationError(detail="사용할 수 없는 이메일입니다.")
    return instance
  
class UserNickDupSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['mb_nickname']
  
  def validate_mb_nickname(self, instance):
    if "admin" in instance:
      raise serializers.ValidationError(detail="사용할 수 없는 닉네임입니다.")
    return instance

class UserFindEmailSerializer(serializers.ModelSerializer):

    class Meta:
      model = get_user_model()
      fields = ['mb_phone']
    
    def validate_mb_phone(self, instance):
      try:
        user = User.objects.filter(mb_phone=instance).values("id", "mb_email", "last_login")
        if len(user) > 0:
          return user
        else: return None
      except:
        return None

class UserPasswordResetSerializer(serializers.ModelSerializer):

  class Meta:
    model = get_user_model()
    password_repeat = serializers.CharField(max_length=255)
    fields = ['id', 'mb_email', 'password']
    extra_kwargs = {
      'password': {'write_only': True}
    }
    
  def validate(self, data):
    if len(data['password']) < 8:
      raise serializers.ValidationError(detail="비밀번호는 8자리 이상 입력해주세요.")
    regex = '^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    if not re.fullmatch(regex, data['password']):
      raise serializers.ValidationError(detail="비밀번호는 영문 + 숫자 + 특수문자 조합으로 입력해주세요.")
    return data
  
  def update(self, instance, validated_data):

    instance.set_password(validated_data.get('password', instance.password))
    instance.save()
    return instance
    
class ExpertSerializer(serializers.ModelSerializer):

  class Meta:
    model = Expert
    fields = ["username", "ep_description", "ep_hours", "ep_education", "ep_license",
              "ep_career", "ep_product", "ep_product_options"]