from django.shortcuts import render
from user.serializer import UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from datetime import datetime

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def create(request):

    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)

    password = data['password']
    password_repeat = data['password_repeat']

    if(password != password_repeat):
        return Response({'password': '비밀번호가 일치하지 않습니다.'}, status=400)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)