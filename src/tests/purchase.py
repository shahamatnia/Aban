from decimal import Decimal

import redis
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from purchase.redis import RedisCli
from src.models import Account
from src.models import Cryptocurrency, PurchaseOrder
from src.services import OrderService


class PurchaseOrderTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')
        self.account = Account.objects.create(user=self.user, balance=100.00)
        self.crypto = Cryptocurrency.objects.create(name='ABAN', price=4.00)
        self.client.force_authenticate(user=self.user)
        # TODO should handle different env for test, for now we just monkeypatch redis!
        RedisCli.pending_cost_prefix = 'test:' + RedisCli.pending_cost_prefix
        RedisCli.primary_redis_client = redis.Redis(host=settings.REDIS_HOST, port=6379, db=15)

    def test_purchase_order_creation(self):
        url = reverse('purchase_orders')
        data = {'cryptocurrency_name': 'ABAN', 'amount': Decimal('3')}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PurchaseOrder.objects.filter(user=self.user, cryptocurrency__name='ABAN').exists())
        updated_account = Account.objects.get(user=self.user)
        self.assertEqual(updated_account.balance, Decimal('88.00'))  # 100 - 3*4

    def test_aggregate_small_orders(self):
        for _ in range(4):
            order = PurchaseOrder.objects.create(
                user=self.user,
                cryptocurrency=self.crypto,
                amount=Decimal('1'),
                status='pending',
            )

            OrderService.aggregate_small_orders(order)
        print(list(map(vars, PurchaseOrder.objects.all())))
        self.assertEqual(PurchaseOrder.objects.filter(status='pending').count(), 1)

    def tearDown(self):
        RedisCli.primary_redis_client.flushdb()
        super().tearDown()
