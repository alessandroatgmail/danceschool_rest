# users/tests/test_users_api.py
# test for the users app
# will test everything around the users management
# create update delete users

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import UserDetails

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')
DETAILS_URL = reverse('users:details')
CREATE_DETAILS_USER = reverse ('users:create_details')


def create_user(**param):
    return get_user_model().objects.create_user(**param)

def create_user_complete(**param):

    user = get_user_model().objects.create_user(
                            email=param['email'],
                            password=param['password']
                            )
    user_details = UserDetails.objects.create(
                    user=user,
                    name='Ale',
                    surname='Silve',
                    address='via roma, 7',
                    city='Maserà',
                    country='Italia',
                    tel='+397532692',
                    privacy=True,
                    marketing=False
    )
    return user, user_details

class PublicUserApiTest(TestCase):
    """Test the user API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ test create user with payload is success"""
        payload = {'email': 'test@seelv.io',
                    'password': 'Test123456!',
                    }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists"""
        payload = {'email':'test@seelv.io',
                    'password': 'test123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 chars"""
        payload = {'email':'test@seelv.io',
                    'password': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test token is create for user"""
        payload = {"email": 'test@selv.io', 'password':'test1234'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token not return if credentials are not valid"""
        payload = {"email": 'test@selv.io', 'password':'test1234'}
        create_user(**payload)
        payload = {"email": 'test@selv.io', 'password':'test12345'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_user_not_exists(self):
        """Test token not return if user does not exists"""
        payload = {"email": 'test@selv.io', 'password':'test1234'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_fields(self):
        """Test that email and password are required"""
        payload = {"email": 'test@selv.io', 'password':''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required to see user details """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_complete(self):
        """Test create user with full details """
        payload = {
            'email':'test@seelv.io',
            'password': 'test12345',
            'user_details':{
            'name':'Ale',
            'surname': 'Silvio',
            'address': 'Via Torino, 5',
            'city': 'Padova',
            'country': 'Italia',
            'tel': '+39049589623',
            'privacy': True,
            'marketing': False
            }
        }

        res = self.client.post(CREATE_DETAILS_USER, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=payload['email'])
        user_details = UserDetails.objects.get(user=user.id)
        self.assertEqual(user_details.surname, payload['user_details']['surname'])

    def test_retrieve_user_details_unauthorized(self):
        """Test that authentication is required to see user details """
        res = self.client.get(DETAILS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """ Test API requests tha require auth"""

    def setUp(self):
        payload = {'email':'test@seelv.io',
                    'password': 'test123',
        }
        self.user=create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """test retriving profile for logged user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
                    res.data,
                    {
                    'email':'test@seelv.io',
                    }
                )

    def test_post_me_not_allowed(self):
        """Test not allowed to post anything"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_simple(self):
        """Test update profile working"""
        payload = {
                    'password': 'new_password',
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_read_user_complete(self):
        """ test restrive all user data """

        user, user_details = create_user_complete(email="ale@seelv.io",
                                                  password='pwd12345')
        self.client.force_authenticate(user=user)
        res = self.client.get(DETAILS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print (user_details)
        self.assertEqual(res.data['email'], user.email)
        self.assertEqual(dict(res.data['user_details']),
                        {
                        'name': user_details.name,
                        'surname': user_details.surname,
                        'address': user_details.address,
                        'city': user_details.city,
                        'country': user_details.country,
                        'tel': user_details.tel,
                        'privacy': user_details.privacy,
                        'marketing': user_details.marketing
                        }
                )
