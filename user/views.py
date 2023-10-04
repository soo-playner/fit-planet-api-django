from rest_framework.renderers import JSONRenderer
from user.serializer import UserPasswordResetSerializer, UserRegisterSerializer, UserSerializer, UserFindEmailSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .validators import *


class OnlyAuthenticatedUserView(APIView):
    permission_classes = [IsAuthenticated]

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        if not user:
            return Response({"error": "접근 권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})

@csrf_exempt
@api_view(['POST'])
def dup_check(request):

    data = JSONParser().parse(request)
    dup_type = data['type']
    value = data['value']

    if not dup_type or not value:
        return Response({'message': '값을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'message': '가입 가능한 ' + dup_type + ' 입니다.'}, status=status.HTTP_200_OK)
    return Response({'message': '중복된 ' + dup_type + ' 입니다.'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def create(request):

    data = JSONParser().parse(request)
    serializer = UserRegisterSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                "data": serializer.data,
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

    serializer = UserFindEmailSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.validated_data['mb_phone'], status=status.HTTP_200_OK)
    return Response({"message": ""}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def reset_password(request):

    data = JSONParser().parse(request)

    if data['password'] != data['password_repeat']:
        return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(mb_email=data['mb_email'])
    serializer = UserPasswordResetSerializer(user, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)