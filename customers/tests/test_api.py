""" Module to test API """
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class UserAPITestCase(TestCase):
    """ Testing API """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_data = {'username': 'testuser', 'password': '12345'}
        self.user_update_data = {'username': 'newtestuser', 'password': 'newpassword'}

    def test_create_user(self):
        """Test creating a new user"""
        response = self.client.post(reverse('user-list'), {
            'username': 'temp_user', 'password': '12345'
        })
        self.assertEqual(response.status_code, 201)

    def test_update_user(self):
        """Test updating a user's username"""
        self.client.login(username='testuser', password='12345')
        response = self.client.put(
            reverse('user-detail', kwargs={'pk': self.user.pk}), self.user_update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(pk=self.user.pk).username, 'newtestuser')

    def test_get_user(self):
        """Test retrieving a user's details"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')

    def test_delete_user(self):
        """Test deleting a user"""
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_jwt_token_obtain_pair(self):
        """Test obtaining JWT token pair"""
        response = self.client.post(reverse('token_obtain_pair'), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_jwt_token_refresh(self):
        """Test refreshing JWT access token"""
        response = self.client.post(reverse('token_obtain_pair'), self.user_data)
        refresh_token = response.data['refresh']
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
