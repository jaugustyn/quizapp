from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, validate_email
from django.contrib.auth import get_user_model
from django.utils import timezone


# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, birth_date, email, password):
        if not email:
            raise ValueError("Email is required field")

        user = self.model(
            email=self.normalize_email(email),
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=100, validators=[validate_email])
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=100, null=False)
    birth_date = models.DateField()
    date_joined = models.DateTimeField(default=timezone.now(), editable=False)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

