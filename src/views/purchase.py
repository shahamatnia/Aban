from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from src.models import Cryptocurrency, Account
from src.serializers import PurchaseOrderSerializer
from django.db import transaction
from django.core.exceptions import ValidationError
from src.services import ExchangeService
from src.services.order import OrderService
from django.conf import settings


class PurchaseOrderView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            amount = serializer.validated_data['amount']
            cryptocurrency_name = serializer.validated_data['cryptocurrency_name']
            cryptocurrency = Cryptocurrency.objects.get(name=cryptocurrency_name)
            price_per_unit = cryptocurrency.price
            total_cost = amount * price_per_unit

            try:
                with transaction.atomic():
                    account = Account.objects.select_for_update().get(user=user)
                    account.deduct_balance(total_cost)
                    purchase_order = serializer.save(user=user, status='pending')

                    if total_cost >= settings.PURCHASE.MIN_COST_INSTANT:
                        ExchangeService.buy_from_exchange(cryptocurrency, amount)
                        purchase_order.status = 'completed'
                        purchase_order.save()
                    else:
                        # TODO: Could Be Async !!
                        OrderService.aggregate_small_orders(purchase_order)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
