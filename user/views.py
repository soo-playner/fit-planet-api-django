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
    
    data =JSONParser().parse(request)
    serializer = UserSerializer(data=data)

    print(f"asd")
    if serializer.is_valid():
        print(f"ddd")

        User.objects.create(mb_id="dmddddkk3m1ccnaver.com",
                            username='dddkkm@dm12cc',
                            is_superuser=1,
                            password='123',
                            first_name='',
                            last_name='',
                            email='asd@naver.com',
                            is_staff=1,
                            is_active=1,
                            date_joined=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return Response(data, status=200)