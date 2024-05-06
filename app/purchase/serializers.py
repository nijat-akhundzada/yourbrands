from rest_framework import serializers
from purchase.models import Order, OrderItem, CanceledOrder


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')


class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_price', 'shipping_address',
                  'additional_notes', 'created_at', 'updated_at', 'items')


class CanceledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanceledOrder
        fields = ('id', 'order', 'reason', 'additional_notes')
