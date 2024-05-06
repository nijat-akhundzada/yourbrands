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
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_address(self, user, pk):
        try:
            return Address.objects.get(user=user, pk=pk)
        except Address.DoesNotExist:
            return None

    def get(self, request, pk):
        address = self.get_address(request.user, pk)
        if address:
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        else:
            return Response({"detail": "Address not found or does not belong to this user."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        address = self.get_address(request.user, pk)
        if address:
            serializer = AddressSerializer(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Address not found or does not belong to this user."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        address = self.get_address(request.user, pk)
        if address:
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Address not found or does not belong to this user."}, status=status.HTTP_404_NOT_FOUND)
