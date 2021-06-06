# booking/tests/test_booking.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

BOOKING_API = reverse('booking:booking')


class PublicBookinApiTests(TestCase):
    """ test public acces to booking api not allowed """

    def setUp(self):
        self.client = APIClient()

    def test_booking_api_not_logged_in(self):
        """test authentication is needed for booking api """
        res = self.client.get(BOOKING_API)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
