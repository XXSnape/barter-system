from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse("users:sign-up")
        data = {"username": "user1", "password": "password123"}
        self.client.post(url, data)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username=data["username"])
        self.assertEqual(user.username, data["username"])
