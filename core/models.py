from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


class CustomUser(AbstractUser):
    phone_number = PhoneField(blank=False, help_text='Contact phone number')

    def __str__(self):
        return self.username
