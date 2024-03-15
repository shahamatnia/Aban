from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')

    def test_obtain_jwt_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'test', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
