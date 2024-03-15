from decimal import Decimal

from django.conf import settings
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Cast

from src.models import PurchaseOrder
from src.services import ExchangeService
from purchase.redis import pending_cost_prefix, primary_redis_client


class OrderService:

    @classmethod
    def _update_pending_amount(cls, order: PurchaseOrder, cost_limit=settings.PURCHASE.MIN_COST_INSTANT):
        """
        Update the total pending amount for a given currency with the current purchase amount.
        If the new total_amount * price exceeds the cost_limit, reset the cache and return the total amount.
        Otherwise, increment the total pending amount by the current amount.


        :param order: The current purchase order.
        :param cost_limit: The limit at which the pending cost triggers an action.
        :return: The total pending amount if the limit is exceeded, else None.
        """

        lua_script = """
        local current_total = redis.call('GET', KEYS[1])
        current_total = current_total and tonumber(current_total) or 0
        local new_total = current_total + tonumber(ARGV[1])
        if new_total >= tonumber(ARGV[2]) then
            redis.call('DEL', KEYS[1])
            return new_total
        else
            redis.call('SET', KEYS[1], new_total)
            return nil
        end
        """

        key = f"{pending_cost_prefix}:{order.cryptocurrency.name}"
        amount_limit = cost_limit / order.cryptocurrency.price
        result = primary_redis_client.eval(lua_script, 1, key, float(order.amount), amount_limit)

        if result:
            return Decimal(result)
        else:
            return None

    @classmethod
    def aggregate_small_orders(cls, order: PurchaseOrder):
        need_to_buy = cls._update_pending_amount(order)
        if not need_to_buy:
            return
        orders = PurchaseOrder.objects.select_for_update().filter(
            cryptocurrency=order.cryptocurrency,
            status='pending',
        )
        total_amount = orders.aggregate(total_amount=Sum('amount'))['total_amount']
        ExchangeService.buy_from_exchange(order.cryptocurrency.name, total_amount)
        orders.update(status='success')
