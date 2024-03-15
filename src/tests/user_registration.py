from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from src.models import Account


class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        """
        Ensure we can create a new user and an account is automatically created.
        """
        url = reverse('create_user')
        data = {'username': 'test', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='test').exists())
        self.assertTrue(Account.objects.filter(user__username='test').exists())
