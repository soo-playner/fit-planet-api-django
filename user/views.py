from user.serializer import *
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
from config.settings.permissions import CustomEmailPermission
from django.shortcuts import get_object_or_404


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

    if data['type'] == 'email':
        serializer = UserEmailDupSerializer(data=data)
    elif data['type'] == 'nickname':
        serializer = UserNickDupSerializer(data=data)

    if serializer.is_valid():
        return Response({'message': '가입 가능한 ' + data['type'] + ' 입니다.'}, status=status.HTTP_200_OK)
    else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @api_view(['PUT'])
# @permission_classes([IsOwner])
# def reset_password(request):

#     data = JSONParser().parse(request)
#     user = get_object_or_404(User, mb_email=data['mb_email'])

#     if data['password'] != data['password_repeat']:
#         return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
#     serializer = UserPasswordResetSerializer(user, data=data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#     else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthDetailView(APIView):

    permission_classes = [CustomEmailPermission]

    def get_object(self, mb_email):
        user = get_object_or_404(User, mb_email=mb_email)
        self.check_object_permissions(self.request, user)
        return user
    
    def put(self, request, mb_email):
        user = self.get_object(mb_email)
        serializer = UserPasswordResetSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)