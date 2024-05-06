from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.serializers import AddressSerializer


class AddressView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get(self, request):
        try:
            address = Address.objects.get(user=request.user)
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except Address.DoesNotExist:
            return Response({"detail": "Address does not exist for this user."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            address = Address.objects.get(user=request.user)
            serializer = AddressSerializer(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"detail": "Address does not exist for this user."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            address = Address.objects.get(user=request.user)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({"detail": "Address does not exist for this user."}, status=status.HTTP_404_NOT_FOUND)
