from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer


class CartItemCreateAPIView(APIView):
    def post(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
