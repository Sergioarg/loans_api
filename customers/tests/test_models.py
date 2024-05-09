""" Moduele to test Models """
from django.test import TestCase
from django.contrib.auth.models import User


class UserModelTest(TestCase):
    """ Testing model User """

    @classmethod
    def setUpTestData(cls):
        UserModelTest.user = User.objects.create_user(
            username='testuser',
            password='123'
        )

    def test_user_creation(self):
        """Test creating a user's username"""
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, 'testuser')

    def test_user_update(self):
        """Test updating a user's username"""
        new_username = 'new_test_username'
        self.user.username = new_username
        self.user.save()
        self.assertEqual(self.user.username, new_username)

    def test_user_delete(self):
        """Test deleting a user"""
        self.user.delete()
        self.assertFalse(User.objects.filter(username='testuser').exists())
