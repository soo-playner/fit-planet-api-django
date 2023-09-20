from user.serializer import UserRegisterSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from django.contrib.auth import authenticate

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def create(request):

    data = JSONParser().parse(request)
    serializer = UserRegisterSerializer(data=data)

    password = data['password']
    password_repeat = data['password_repeat']

    if(password != password_repeat):
        return Response({'password': '비밀번호가 일치하지 않습니다.'}, status=400)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "user": serializer.data,
            },
            status=200
        )
    return Response(serializer.errors, status=400)


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
            "user": "아이디 혹은 비밀번호를 잘못 입력하셨습니다.",
        },status=status.HTTP_400_BAD_REQUEST)