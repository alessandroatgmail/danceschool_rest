# core/tests/test_core.py
# this will test everything around the models like creating updating and
# deleting rows in the database

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@seelv.io'
        password = 'Password123'
        user = get_user_model().objects.create_user(
			email=email,
			password=password
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
