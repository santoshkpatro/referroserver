from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/phone/', views.login_phone, name='login_phone'),
    path('login/phone/verify/', views.login_phone_verify, name='login_phone_verify'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]
