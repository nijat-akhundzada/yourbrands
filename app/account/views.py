from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser, OTP
from account.serializers import CustomUserSerializer, MyTokenObtainPairSerializer, SendOTPSerializer, PostSerializer, ResetPasswordSerializer, ChangePasswordSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

import os
from twilio.rest import Client
import random
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(
    description="Send OTP to the provided phone number.", request=SendOTPSerializer
)
@api_view(['POST',])
def send_otp(request):
    phone_number = request.data.get('mobile_number')
    if not phone_number:
        return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])

    try:
        client = Client(os.environ.get('twilio_account_SID'),
                        os.environ.get("twilio_auth_token"))

        client.messages.create(
            body=f'Your OTP for authentication is {otp}',
            from_=os.environ.get('twilio_phone_number'),
            to=phone_number
        )
        print(otp)
    except Exception as e:
        return Response({'message': f'Error sending OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    otp_obj = OTP.objects.create(otp=otp,
                                 expiration_time=timezone.now() + timezone.timedelta(minutes=180))
    return Response({'message': 'OTP sent to the phone number', 'otp_id': otp_obj.pk}, status=status.HTTP_200_OK)


class CustomUserListCreateAPIView(APIView):

    @extend_schema(
        request=CustomUserSerializer
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PostSerializer
    )
    def post(self, request):
        otp_entered = request.data.get('otp')
        otp_id = request.data.get('otp_id')

        if not (otp_entered and otp_id):
            return Response({'message': 'Phone number, OTP, and OTP ID are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            otp_obj = OTP.objects.get(
                pk=otp_id, otp=otp_entered)
        except OTP.DoesNotExist:
            return Response({'message': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verify the OTP
        if str(otp_entered) != otp_obj.otp:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP is expired
        if otp_obj.is_expired():
            return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        # If OTP is valid, create the user
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            otp_obj.delete()  # Delete OTP object after successful verification
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=ChangePasswordSerializer
)
@api_view(['POST',])
def change_password(request):
    user = request.user

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'message': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


@extend_schema(
    request=SendOTPSerializer
)
@api_view(['POST',])
def forgot_password(request):
    phone_number = request.data.get('mobile_number')
    if not phone_number:
        return Response({'message': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])

    try:
        # Send OTP to the provided phone number
        client = Client(os.environ.get('twilio_account_SID'),
                        os.environ.get("twilio_auth_token"))

        client.messages.create(
            body=f'Your OTP for password reset is {otp}',
            from_=os.environ.get('twilio_phone_number'),
            to=phone_number
        )
    except Exception as e:
        return Response({'message': f'Error sending OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    otp_obj = OTP.objects.create(otp=otp,
                                 expiration_time=timezone.now() + timezone.timedelta(minutes=5))

    return Response({'message': 'OTP sent to the phone number', 'otp_id': otp_obj.pk}, status=status.HTTP_200_OK)


@extend_schema(
    request=ResetPasswordSerializer
)
@api_view(['POST',])
def reset_password(request):
    otp_entered = request.data.get('otp')
    otp_id = request.data.get('otp_id')
    new_password = request.data.get('new_password')
    phone_number = request.data.get('mobile_number')

    if not (otp_entered and otp_id and new_password):
        return Response({'message': 'OTP, OTP ID, and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        otp_obj = OTP.objects.get(
            pk=otp_id, otp=otp_entered)
    except OTP.DoesNotExist:
        return Response({'message': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)

    # Verify the OTP
    if str(otp_entered) != otp_obj.otp:
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if OTP is expired
    if otp_obj.is_expired():
        return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.get(mobile_number=phone_number)

    if not user:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Set the new password
    user.set_password(new_password)
    user.save()

    # Delete OTP object after successful password reset
    otp_obj.delete()

    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
