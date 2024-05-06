from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from purchase.models import Order, OrderItem, CanceledOrder
from purchase.serializers import OrderSerializer, OrderItemSerializer, CanceledOrderSerializer
from rest_framework.permissions import IsAuthenticated


class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_order(self, user, order_id):
        try:
            return Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return None

    def get(self, request, order_id):
        order = self.get_order(request.user, order_id)
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, order_id):
        order = self.get_order(request.user, order_id)
        if order:
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, order_id):
        order = self.get_order(request.user, order_id)
        if order:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class CanceledOrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        canceled_orders = CanceledOrder.objects.all()
        serializer = CanceledOrderSerializer(canceled_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CanceledOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
