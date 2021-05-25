from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and saves a new users
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates and saves a new superusers"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model that support email instead username
    """
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserDetails(models.Model):
    """ Models containing user details """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
        )
    name = models.CharField(max_length=255, blank=False)
    surname = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=255, blank=False)
    country = models.CharField(max_length=255, blank=False)
    tel = models.CharField(max_length=13, blank=False)
    privacy = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)


class Location(models.Model):
    """ Model for event location  """
    name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=255, blank=False)
    room = models.CharField(max_length=255)


class Artist(models.Model):
    """Model with bio details of artists """
    name = models.CharField(max_length=255, blank=False)
    style = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    country = models.CharField(max_length=50, blank=False)


class Event(models.Model):
    """Model with single event detail """
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)
