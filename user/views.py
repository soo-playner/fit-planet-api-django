from user.serializer import UserRegisterSerializer, UserSerializer, UserPasswordSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .validators import *
from django.core import serializers
import re

@csrf_exempt
@api_view(['POST'])
def dup_check(request):

    data = JSONParser().parse(request)
    dup_type = data['type']
    value = data['value']

    if not dup_type or not value:
        return Response({'message': '값을 입력해주세요.'}, status=400)

    if dup_type == 'email':
        try:
            _duplicated = User.objects.get(mb_email=value)
        except:
            _duplicated = None
    elif dup_type == 'nickname':
        try:
            _duplicated = User.objects.get(mb_nickname=value)
        except:
            _duplicated = None
    if _duplicated is None:
        return Response({'message': 'not duplicated'}, status=200)
    return Response({'message': 'deplicated value'}, status=400)


@csrf_exempt
@api_view(['POST'])
def create(request):

    data = JSONParser().parse(request)
    serializer = UserRegisterSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "user": serializer.data,
            },
            status=200
        )
    return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
def login(request):

    username = request.data.get('mb_email')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        serializer = UserSerializer(user)
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        return Response(
            {
                "user": serializer.data,
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response({
            "message": "아이디 혹은 비밀번호를 잘못 입력하셨습니다.",
        },status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['POST'])
def find_id(request):

    data = JSONParser().parse(request)
    mb_phone = data['mb_phone']
    auth_number = data['auth_number']

    if not mb_phone:
        return Response({
            "message": "값을 입력해주세요"
        },status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(mb_phone=mb_phone).values("mb_email")
    if len(user) > 0:
        return Response(user, status=status.HTTP_200_OK)
    else: return Response({
            "message": "일치하는 회원이 없습니다."
        },status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def reset_password(request):

    data = JSONParser().parse(request)
    mb_email = data["mb_email"]
    password = data["password"]
    password_repeat = data["password_repeat"]

    if not mb_email:
        return Response({
            "message": "값을 입력해주세요"
        },status=status.HTTP_400_BAD_REQUEST)
    
    if password != password_repeat:
        return Response({
            "message": "비밀번호가 일치하지 않습니다."
        },status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 8:
        return Response({
            "message": "비밀번호가 일치하지 않습니다."
        },status=status.HTTP_400_BAD_REQUEST)
    regex = '^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    if not re.fullmatch(regex, password):
        return Response({
            "message": "비밀번호 입력 양식을 확인해주세요."
        },status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(mb_email=mb_email)
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response({
            "message": "일치하는 회원이 없습니다."
        },status=status.HTTP_400_BAD_REQUEST)
