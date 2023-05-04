from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
    PermissionsMixin
)


class UserManager(UserManager):

    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError("Username field cannot be empty. ")
        if email is None:
            raise TypeError("Email field cannot be empty. ")
        if password is None:
            raise TypeError("Please enter password. ")

        user = self.create_user(username, email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Username field cannot be empty. ")
        if email is None:
            raise TypeError("Email field cannot be empty. ")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


# AUTH_PROVIDERS = {
# 	'email': 'email'
# }

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # auth_provider = models.CharField(
    # 	max_length=255,
    # 	blank=False,
    # 	null=False,
    # 	default=AUTH_PROVIDERS.get('email')
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.username
