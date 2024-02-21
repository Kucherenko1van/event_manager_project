from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Event


class UserAccountTests(APITestCase):

    def test_register_user(self):
        url = reverse("register_user")
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "user@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        User.objects.create_user(username="testuser", password="testpassword123")
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_token_refresh(self):
        user = User.objects.create_user(username="testuser", password="testpassword123")
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")
        refresh_token = response.data["refresh"]

        refresh_url = reverse("token_refresh")
        refresh_data = {"refresh": refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data, format="json")
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in refresh_response.data)


class UserEventTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword123"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword1234"
        )
        url = reverse("token_obtain_pair")
        resp = self.client.post(
            url, {"username": "testuser1", "password": "testpassword123"}, format="json"
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + resp.data["access"])
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            start_date="2023-01-01T00:00:00Z",
            end_date="2023-01-02T00:00:00Z",
            creator=self.user1,
        )

    def test_user_can_edit_own_event(self):
        url = reverse("event-detail", kwargs={"pk": self.event.pk})
        data = {
            "name": "Updated Event",
            "description": "Updated Description",
            "start_date": "2023-01-03T00:00:00Z",
            "end_date": "2023-01-04T00:00:00Z",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Updated Event")

    def test_user_cannot_edit_others_event(self):
        self.client.force_authenticate(user=self.user2)  # Switch to user2
        url = reverse("event-detail", kwargs={"pk": self.event.pk})
        data = {
            "name": "Attempted Unauthorized Update",
            "description": "Should Fail",
            "start_date": "2023-01-03T00:00:00Z",
            "end_date": "2023-01-04T00:00:00Z",
        }
        response = self.client.put(url, data, format="json")

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


class EventFilterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="filteruser", password="filterpassword"
        )
        url = reverse("token_obtain_pair")
        data = {"username": "filteruser", "password": "filterpassword"}
        response = self.client.post(url, data, format="json")
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        Event.objects.create(
            name="New Year Party",
            description="Celebrating the new year",
            start_date="2023-12-31T00:00:00Z",
            end_date="2024-01-01T00:00:00Z",
            creator=self.user,
        )
        Event.objects.create(
            name="Tech Conference",
            description="Annual tech conference",
            start_date="2023-11-15T00:00:00Z",
            end_date="2023-11-17T00:00:00Z",
            creator=self.user,
        )
        Event.objects.create(
            name="Summer Festival",
            description="Outdoor music and arts festival",
            start_date="2023-08-05T00:00:00Z",
            end_date="2023-08-07T00:00:00Z",
            creator=self.user,
        )

    def test_filter_events_by_name(self):
        url = reverse("event-list") + "?name=conference"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("Tech Conference", response.data[0]["name"])

    def test_filter_events_by_start_date(self):
        url = reverse("event-list") + "?start_date=2023-09-01"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for event in response.data:
            self.assertTrue(event["start_date"] >= "2023-09-01T00:00:00Z")

    def test_filter_events_by_date_range(self):
        url = reverse("event-list") + "?start_date=2023-07-01&end_date=2023-08-31"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("Summer Festival", response.data[0]["name"])


class UserEventRegistrationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            start_date="2023-01-01T00:00:00Z",
            end_date="2023-01-02T00:00:00Z",
            creator=self.user,
        )

    def test_register_for_event(self):
        url = reverse("event-register", kwargs={"pk": self.event.pk})
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.event.attendees.filter(pk=self.user.pk).exists())

    def test_unregister_from_event(self):
        self.event.attendees.add(self.user)
        url = reverse("event-unregister", kwargs={"pk": self.event.pk})
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.event.attendees.filter(pk=self.user.pk).exists())
