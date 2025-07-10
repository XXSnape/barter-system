from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from ads.models import Ad, ExchangeProposal


class ProposalTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user1 = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.user2 = User.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        cls.user3 = User.objects.create_user(
            username="testuser3", password="testpassword3"
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
            user=cls.user2,
        )
        cls.ad3 = Ad.objects.create(
            title="Sample Ad 3",
            description="This is a third sample ad description.",
            category="Sample Category",
            condition="New",
            user=cls.user1,
        )

        cls.proposal1 = ExchangeProposal.objects.create(
            ad_sender=cls.ad1,
            ad_receiver=cls.ad2,
            comment="Looking to exchange",
        )

    @classmethod
    def tearDownClass(cls):
        cls.user1.delete()
        cls.user2.delete()
        cls.user3.delete()
        cls.ad1.delete()

    def setUp(self):
        self.client.force_login(self.user1)

    def test_list_proposals(self):
        url = reverse("ads:proposals-list")
        response = self.client.get(url)
        self.assertQuerySetEqual(
            qs=ExchangeProposal.objects.all(),
            values=[proposal["id"] for proposal in response.json()["results"]],
            transform=lambda proposal: proposal.pk,
        )

    def test_no_receiver_and_sender_proposals(self):
        url = reverse("ads:proposals-list")
        self.client.force_login(self.user3)
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json["results"]), 0)

    def test_retrieve_proposal(self):
        url = reverse("ads:proposals-detail", args=[self.proposal1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["id"], self.proposal1.pk)
        self.assertEqual(json["ad_sender"], self.ad1.pk)
        self.assertEqual(json["ad_receiver"], self.ad2.pk)

    def test_retrieve_proposal_no_receiver_and_sender(self):
        url = reverse("ads:proposals-detail", args=[self.proposal1.pk])
        self.client.force_login(self.user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_proposal(self):
        url = reverse("ads:proposals-list")
        data = {
            "ad_sender": self.ad3.pk,
            "ad_receiver": self.ad2.pk,
            "comment": "Interested in exchanging",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExchangeProposal.objects.count(), 2)
        new_proposal = ExchangeProposal.objects.last()
        self.assertEqual(new_proposal.ad_sender, self.ad3)
        self.assertEqual(new_proposal.ad_receiver, self.ad2)

    def test_cant_create_proposal(self):
        url = reverse("ads:proposals-list")
        data = {
            "ad_sender": self.ad2.pk,
            "ad_receiver": self.ad1.pk,
            "comment": "Interested in exchanging",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_update_proposal(self):
        self.client.force_login(self.user2)
        url = reverse("ads:proposals-detail", args=[self.proposal1.pk])
        data = {
            "status": "Принято",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.proposal1.refresh_from_db()
        self.assertEqual(self.proposal1.status, "Принято")

    def test_update_no_receiver(self):
        self.client.force_login(self.user1)
        url = reverse("ads:proposals-detail", args=[self.proposal1.pk])
        data = {
            "status": "Принято",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403)

    def test_delete_proposal(self):
        url = reverse("ads:proposals-detail", args=[self.proposal1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            ExchangeProposal.objects.filter(pk=self.proposal1.pk).exists()
        )

    def test_cant_delete_proposal(self):

        self.client.force_login(self.user2)
        url = reverse("ads:proposals-detail", args=[self.proposal1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            ExchangeProposal.objects.filter(pk=self.proposal1.pk).exists()
        )
