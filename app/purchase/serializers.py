from rest_framework import serializers
from purchase.models import Order, OrderItem, CanceledOrder
from address.models import Address


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity')


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all())
    additional_notes = serializers.CharField(max_length=255, allow_blank=True)
    is_paid = serializers.BooleanField()

    items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.total_price = validated_data.get(
            'total_price', instance.total_price)
        instance.shipping_address = validated_data.get(
            'shipping_address', instance.shipping_address)
        instance.additional_notes = validated_data.get(
            'additional_notes', instance.additional_notes)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()

        items_data = validated_data.get('items', [])
        instance.items.all().delete()  # Remove existing items
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)
        return instance


class CanceledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanceledOrder
        fields = ('id', 'order', 'reason', 'additional_notes')
