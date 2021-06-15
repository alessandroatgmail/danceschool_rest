from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from datetime import date


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
        primary_key=True,
        related_name='user_details'
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

    def __str__(self):

        return self.name


class Artist(models.Model):
    """Model with bio details of artists """
    name = models.CharField(max_length=255, blank=False)
    style = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    country = models.CharField(max_length=50, blank=False)

    def __str__(self):

        return self.name


class Event(models.Model):
    """Model with single event detail """
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):

        return self.name

class Discount(models.Model):
    """Model for discount apply to the package """
    name = models.CharField(max_length=255, blank=False)
    discount = models.DecimalField(max_digits=4, decimal_places=2)

class Pack(models.Model):
    """Model for package, a package is a list of events for purchase """
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    events = models.ManyToManyField(Event, blank=True, null=True)
    discounts = models.ManyToManyField(Discount, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):

        return self.name

    @property
    def starting_date(self):

        return min([event.date for event in self.events.all()])


class Booking(models.Model):
    users = models.ForeignKey(User, on_delete=models.PROTECT)
    packs = models.ForeignKey(Pack, on_delete=models.PROTECT)
    date = models.DateField(default=date.today().strftime("%Y-%m-%d"))
    payed = models.BooleanField(default=False)
    date_payed = models.DateField(null=True, blank=True)
