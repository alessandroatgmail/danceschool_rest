# booking/tests/test_booking.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core import models

BOOKING_API = reverse('booking:booking')

# helper functions

def create_user(**param):
    return get_user_model().objects.create_user(**param)

def create_location(**param):
    return models.Location.objects.create(**param)

def create_artist(**param):
    return models.Artist.objects.create(**param)

def create_event(**param):
    artists = param.pop('artists')
    event = models.Event.objects.create(**param)
    for artist in artists:
        event.artist.add(artist)
    event.save()
    return event

def create_pack(**param):
    events = param.pop('events')
    pack = models.Pack.objects.create(**param)
    for event in events:
        pack.events.add(event)
    pack.save()
    return pack


class PublicBookinApiTests(TestCase):
    """ test public acces to booking api not allowed """

    def setUp(self):
        self.client = APIClient()

    def test_booking_api_not_logged_in(self):
        """test authentication is needed for booking api """
        res = self.client.get(BOOKING_API)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookingTests(TestCase):
    """Test private booking api"""

    def setUp(self):
        payload = {'email':'test@seelv.io',
                    'password': 'test123',
        }
        self.user=create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        location = create_location(
                    name="Carichi",
                    address='via portello 1',
                    city='Padova',
                    room='main'
                    )
        self.artist1 = create_artist(
                name="Frankie Manning",
                type="Teacher",
                style="Lindy Hop",
                description = "",
                country="USA",
        )

        self.artist2 = create_artist(
                name="Count Basie",
                type="Band",
                style="Big Band Swing",
                description = "",
                country="USA",
        )

        self.event1 = create_event(
            name="Bounce Factory",
            type="Weekely beginner Class",
            date="2021-05-18",
            time="21:00",
            description="Lezione beginner livello 1 più social dance dalle 23.00",
            price = 10.0,
            location=location,
            artists=[self.artist1, self.artist2]

        )

        self.event2 = create_event(
            name="Bounce Factory After class Social",
            type="Social Dance",
            date="2021-05-18",
            time="21:00",
            description="Social dance with band and dj set",
            price = 10.0,
            location=location,
            artists=[self.artist1, self.artist2]

        )

        self.pack = create_pack (
                name="Bounce Factory all night",
                price=15.0,
                events=[self.event1, self.event2]
        )



    def test_access_booking_api_auth(self):

        """test authentication is needed for booking api """
        res = self.client.get(BOOKING_API)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_packs_api(self):

        """test retrive a list of packages """
        res = self.client.get(BOOKING_API)
        print("Date")
        print (res.data[0]['events'][0]['date'])
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], 'Bounce Factory all night')
        self.assertEqual(res.data[0]['events'][0]['date'],
                         min([self.event1.date, self.event2.date])
                         )
        self.assertEqual(res.data[0]['events'][0]['artist'][0]['name'], self.artist1.name)
