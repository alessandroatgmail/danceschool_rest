# booking/views.py
from rest_framework import generics, authentication, permissions, \
                            viewsets, mixins
from booking.serializers import PackListSerializers
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class BookingPackList(generics.ListAPIView):
    """Create a new user in the system """
    serializer_class = PackListSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
