# users/tests/test_users_api.py
# test for the users app
# will test everything around the users management
# create updat delete users


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
