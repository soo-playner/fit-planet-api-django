from rest_framework.permissions import BasePermission
from rest_framework.parsers import JSONParser
from rest_framework import permissions


class CustomEmailPermission(BasePermission):

  def has_permission(self, request, view):

    return request.user and request.user.is_authenticated
  
  def has_object_permission(self, request, view, obj):

    print(obj.mb_email)
    print(request.user)

    return obj.mb_email == str(request.user)