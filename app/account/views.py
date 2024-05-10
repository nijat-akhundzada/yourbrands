from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser, Wishlist
from account.serializers import CustomUserSerializer, MyTokenObtainPairSerializer, ResetPasswordSerializer, ChangePasswordSerializer, WishlistSerializer
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserListCreateAPIView(APIView):

    serializer_class = CustomUserSerializer

    # def get(self, request):
    #     users = CustomUser.objects.all()
    #     serializer = CustomUserSerializer(users, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
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
    request=ResetPasswordSerializer
)
@api_view(['POST',])
def reset_password(request):
    new_password = request.data.get('new_password')
    phone_number = request.data.get('mobile_number')

    user = CustomUser.objects.get(mobile_number=phone_number)

    if not user:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Set the new password
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


class WishlistView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = WishlistSerializer

    def get(self, request):
        wishlist = get_object_or_404(Wishlist, user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_ids = request.data.get('products', [])
        if product_ids:
            wishlist.products.add(*product_ids)
            wishlist.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response({"error": "Product IDs are required"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def wishlist_product_delete(request, pk):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    try:
        wishlist.products.remove(pk)
        wishlist.save()
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
