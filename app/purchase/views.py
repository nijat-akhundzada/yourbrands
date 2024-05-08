from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from purchase.models import Order, OrderItem, CanceledOrder
from purchase.serializers import OrderSerializer,  CanceledOrderSerializer
from address.models import Address
from product.models import Product


class OrderListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def post(self, request):
        data = request.data
        try:
            user = request.user
            address_id = data.get('address_id')
            address = Address.objects.get(id=address_id)

            total_price = data.get('total_price')

            order = Order.objects.create(
                user=user,
                total_price=total_price,
                shipping_address=address,
                additional_notes=data.get('additional_notes', '')
            )

            for item_data in data.get('items', []):
                product_id = item_data.get('product_id')
                product = Product.objects.get(id=product_id)
                quantity = item_data.get('quantity')
                price = product.discounted_price()

                if product.stock >= quantity:
                    product.stock -= quantity
                    product.save()
                else:
                    order.delete()
                    return Response({'error': f'Not enough stock available for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CanceledOrderCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CanceledOrderSerializer

    def post(self, request):
        data = request.data
        try:
            order_item_id = data.get('order_item_id')
            order_item = OrderItem.objects.get(id=order_item_id)
            reason = data.get('reason')
            additional_notes = data.get('additional_notes', '')

            order_item.product.quantity += order_item.quantity
            order_item.product.save()

            order_item.order.status = 'Ləğv edildi'
            order_item.order.save()

            canceled_order = CanceledOrder.objects.create(
                order=order_item,
                reason=reason,
                additional_notes=additional_notes
            )
            serializer = CanceledOrderSerializer(canceled_order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
