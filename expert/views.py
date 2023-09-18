from expert.serializer import ExpertSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def create(request):
    
    data = JSONParser().parse(request)
    serializer = ExpertSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)