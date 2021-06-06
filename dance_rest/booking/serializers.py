# booking/serializers.py

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from core.models import Pack


class PackListSerializers(serializers.ModelSerializer):

    model = Pack
    fields = ['name', 'description', 'events', 'price']
    extra_kwargs = {'select': {'write_only':True, 'min_length':5}}
