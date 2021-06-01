from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from core.models import UserDetails


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {'password':
            {'write_only':True, 'min_length':5}
        }

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs


class DetailsSerializer(serializers.ModelSerializer):
    """ serialiazer for user_details """

    class Meta:
        model = UserDetails
        fields = ('user', 'name', 'surname')


class UserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for the details object"""

    user_details = DetailsSerializer(
        many=False, read_only=True
        # queryset=UserDetails.objects.all()
    )

    class Meta:
        model = get_user_model()
        # model = UserDetails
        fields = ['id', 'email', 'user_details', ]
        # fields = ['name', 'surname', 'user__email']
        # read_only_fields = ('id',)
        # read_only_fields = ('user')





# class UserDetailsSerializerComplete(serializers.ModelSerializer):
#     """ serialiazer for complete user + details """
#
#     cl
