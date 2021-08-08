from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


@api_view(('POST',))
def login_phone(request):
    try:
        user = User.objects.get(phone=request.data['phone'])
        print(user.generate_phone_otp())
        return Response(status=status.HTTP_200_OK, data={'detail': 'OTP has been sent to your mobile number'})
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Phone number not found'})


@api_view(('POST',))
def login_phone_verify(request):
    try:
        user = User.objects.get(phone=request.data['phone'])
        otp = request.data['otp']
        if user.verify_phone_otp(otp):
            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)
            user.reset_counter()
            return Response(status=status.HTTP_200_OK, data={'access': str(access), 'refresh': str(refresh)})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': 'OTP verification failed'})
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Phone number not found'})


class ProfileView(APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
