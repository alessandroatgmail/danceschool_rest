# core/tests/test_core.py
# this will test everything around the models like creating updating and
# deleting rows in the database

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import UserDetails, Location, Artist, Event

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@seelv.io'
        password = 'Password123'

        user = get_user_model().objects.create_user(
			email=email,
			password=password,
		)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        """Test if new user email is normalized"""
        email = 'test@SEELV.io'
        password = 'Password123'
        user = get_user_model().objects.create_user(
			email=email,
			password=password
		)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):

        """ test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superusers(self):
        """Test create Superuser"""
        user = get_user_model().objects.create_superuser(
            "test_admin@seelv.io",
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_details(self):
        email = 'test@seelv.io'
        password = 'Password123'
        name = 'Ale'
        surname = 'Rossi'
        address = 'via v. veneto, 4'
        tel = '+395691215'
        city = 'Milano'
        country = 'Germany'
        privacy = True
        marketing = False

        user = get_user_model().objects.create_user(
			email=email,
			password=password,

		)

        user_details = UserDetails.objects.create(
            user=user,
            name=name,
            surname=surname,
            address=address,
            tel=tel,
            city=city,
            country=country,
            privacy=privacy,
            marketing=marketing
        )
        self.assertEqual(user_details.name, name)
        self.assertEqual(user_details.surname, surname)
        self.assertEqual(user_details.address, address)
        self.assertEqual(user_details.city, city)
        self.assertEqual(user_details.country, country)
        self.assertEqual(user_details.privacy, privacy)
        self.assertEqual(user_details.marketing, marketing)

    def test_create_location(self):
        """Test the creation of location event model"""
        name = "Carichi Sospesi"
        address = "vic. Portello 1"
        city = "Padova"
        room = "Main"
        location = Location.objects.create(
            name=name,
            address=address,
            city=city,
            room=room
        )

        self.assertEqual(location.name, name)
        self.assertEqual(location.address, address)
        self.assertEqual(location.city, city)
        self.assertEqual(location.room, room)


    def test_create_artist(self):
        """Test creation of artist"""
        name = "Frankie Manning"
        type = "Teacher"
        style = "Lindy Hop"
        description = ""
        country = "United Kingdom"

        artist = Artist.objects.create(
            name=name,
            type=type,
            style=style,
            description=description,
            country=country
        )

        self.assertEqual(artist.name, name)
        self.assertEqual(artist.type, type)
        self.assertEqual(artist.style, style)
        self.assertEqual(artist.description, description)
        self.assertEqual(artist.country, country)

    def test_create_events(self):
        """Test creation events"""

        # first create the Location

        name = "Carichi Sospesi"
        address = "vic. Portello 1"
        city = "Padova"
        room = "Main"
        location = Location.objects.create(
            name=name,
            address=address,
            city=city,
            room=room
        )

        event_name = "Bounce Factory"
        event_type = "Weekely beginner Class"
        event_date = "2021-05-18"
        event_time = "21:00"
        event_description = "Lezione beginner livello 1 più social dance dalle 23.00"

        event = Event.objects.create(
            name=event_name,
            type=event_type,
            date=event_date,
            time=event_time,
            description=event_description,
            location=location
        )

        # create two artists and add to the event

        name = "Frankie Manning"
        type = "Teacher"
        style = "Lindy Hop"
        description = ""
        country = "United Kingdom"

        artist = Artist.objects.create(
            name=name,
            type=type,
            style=style,
            description=description,
            country=country
        )

        name = "Count Basie"
        type = "Band"
        style = "Swing"
        description = ""
        country = "USA"

        artist2 = Artist.objects.create(
            name=name,
            type=type,
            style=style,
            description=description,
            country=country
        )

        event.artist.add(artist)
        event.artist.add(artist2)
        event.save()
        print (event.artist.all())

        self.assertEqual(event.name, event_name)
        self.assertEqual(event.type, event_type)
        self.assertEqual(event.date, event_date)
        self.assertEqual(event.time, event_time)
        self.assertEqual(event.description, event_description)
        self.assertIn(artist, event.artist.all())
