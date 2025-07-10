from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ads.models import Ad


class AdTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user1 = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.user2 = User.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        cls.ad1 = Ad.objects.create(
            title="Sample Ad 1",
            description="This is a sample ad description.",
            category="Sample Category",
            condition="New",
            user=cls.user1,
        )
        cls.ad2 = Ad.objects.create(
            title="Sample Ad 2",
            description="This is another sample ad description.",
            category="Sample Category",
            condition="Used",
            user=cls.user1,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user1.delete()
        cls.user2.delete()

    def setUp(self):
        self.client.force_login(self.user1)

    def test_list_ads(self):
        """
        Ensure we can retrieve a list of ads.
        """
        url = reverse("ads:ad-list")
        response = self.client.get(url)
        self.assertQuerySetEqual(
            qs=Ad.objects.all(),
            values=[ad["id"] for ad in response.json()["results"]],
            transform=lambda ad: ad.pk,
        )

    def test_retrieve_ad(self):

        url = reverse("ads:ad-detail", kwargs={"pk": self.ad1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        del json["created_at"]

        self.assertEqual(
            {
                "id": self.ad1.pk,
                "title": self.ad1.title,
                "description": self.ad1.description,
                "category": self.ad1.category,
                "condition": self.ad1.condition,
                "image_url": None,
                "username": self.user1.username,
            },
            response.json(),
        )

    def test_create_ad(self):
        url = reverse("ads:ad-list")
        data = {
            "title": "Test Ad",
            "description": "This is a test ad description.",
            "category": "Test Category",
            "condition": "New",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(Ad.objects.count(), 3)

    def test_update_ad(self):
        url = reverse("ads:ad-detail", kwargs={"pk": self.ad1.pk})
        response = self.client.patch(url, {"title": "Updated Ad Title"})
        self.assertEqual(response.status_code, 200)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, "Updated Ad Title")

    def test_delete_ad(self):
        url = reverse("ads:ad-detail", kwargs={"pk": self.ad1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Ad.objects.filter(pk=self.ad1.pk).exists())

    def test_fail_delete_ad(self):
        url = reverse("ads:ad-detail", kwargs={"pk": self.ad2.pk})
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Ad.objects.filter(pk=self.ad2.pk).exists())
