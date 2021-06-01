from rest_framework import generics, authentication, permissions, \
                            viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework.settings import api_settings
from users.serializers import UserSerializer, AuthTokenSerializer, \
                              UserDetailsSerializer
from rest_framework.views import APIView
from core.models import UserDetails
from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """return and return authenticated user """
        return self.request.user


class ManageDetailsUserView(viewsets.ModelViewSet, mixins.RetrieveModelMixin):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated,]
    # lookup_field = 'id'
    queryset = get_user_model().objects.all()
    # def get_queryset(self):
    #     return self.request.user.user_details

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

# class ManageDetailsUserView(generics.RetrieveUpdateAPIView):
#     """manage the authenticated user """
#     queryset = get_user_model().objects.all()
#
#     serializer_class = UserDetailsSerializer
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_queryset(self):
#         """Retrieve the recipes for the authenticated user"""
#         return self.queryset.filter(email=self.request.user)
