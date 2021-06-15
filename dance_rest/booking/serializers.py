# booking/serializers.py

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from core.models import Pack, Event, Artist


class EventArtistListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['name', 'style', 'type', 'country']

class PackEventListSerializers(serializers.ModelSerializer):

    artist = EventArtistListSerializers(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ['date', 'type', 'description', 'time',
                  'location', 'artist', 'price']





class PackListSerializers(serializers.ModelSerializer):

    events = PackEventListSerializers(read_only=True, many=True)

    class Meta:
        model = Pack
        fields = ['name', 'description',
                  'events',
                  # 'dates',
                  'price']
        extra_kwargs = {'select': {'write_only':True, 'min_length':5}}
