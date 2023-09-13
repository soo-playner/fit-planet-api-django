from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    username = serializers.EmailField(source="user.username",required=True)
    
    class Meta:
        model = get_user_model()
        fields = ["username"]

    
