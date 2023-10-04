from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('dup-check/', views.dup_check, name="dup_check"),
    path('create/', views.create, name="create"),
    path('login/', views.login, name="login"),
    path('find-id/', views.find_id, name="find_id"),
    path('reset-password/', views.reset_password, name="reset_password"),
    path('jwt-auth/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('jwt-auth/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('jwt-auth/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('jwt-auth/authonly/', views.OnlyAuthenticatedUserView.as_view()),
]