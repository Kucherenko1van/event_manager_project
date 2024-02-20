from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Event
from rest_framework.authtoken.models import Token


class UserTest(APITestCase):

    def test_register_user(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class EventAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.event_data = {
            "name": "Test Event",
            "description": "Test Description",
            "start_date": "2023-01-01T00:00:00Z",
            "end_date": "2023-01-02T00:00:00Z",
        }

    def test_create_event(self):
        url = reverse("event-list")
        self.event_data["creator"] = self.user.pk
        response = self.client.post(url, self.event_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().name, "Test Event")

    def test_get_event_list(self):
        Event.objects.create(**self.event_data, creator=self.user)
        url = reverse("event-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_event(self):
        event = Event.objects.create(**self.event_data, creator=self.user)
        url = reverse("event-detail", kwargs={"pk": event.pk})
        updated_data = {
            "name": "Updated Event",
            "description": "Updated Description",
            "start_date": "2023-01-01T00:00:00Z",
            "end_date": "2023-01-02T00:00:00Z",
            "creator": self.user.pk,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.name, "Updated Event")

    def test_delete_event(self):
        event = Event.objects.create(**self.event_data, creator=self.user)
        url = reverse("event-detail", kwargs={"pk": event.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)


class EventFilterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        Event.objects.create(
            name="New Year Party",
            description="Celebrating the new year",
            start_date="2023-12-31",
            end_date="2024-01-01",
            creator=self.user,
        )
        Event.objects.create(
            name="Conference",
            description="Tech conference",
            start_date="2023-11-10",
            end_date="2023-11-12",
            creator=self.user,
        )
        Event.objects.create(
            name="Birthday Party",
            description="My birthday party",
            start_date="2023-05-23",
            end_date="2023-05-23",
            creator=self.user,
        )

    def test_filter_events_by_name(self):
        url = reverse("event-list") + "?name=party"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_events_by_start_date(self):
        url = reverse("event-list") + "?start_date=2023-06-01"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_events_by_date_range(self):
        url = reverse("event-list") + "?start_date=2023-01-01&end_date=2023-12-30"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
