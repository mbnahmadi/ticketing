from django.db import models
from django .contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
    ("m", "male"),
    ("f", "female")
)

class UserModel(AbstractUser):
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    gender = models.CharField(choices=GENDER_CHOICES, null=False, blank=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.username}- {self.first_name} {self.last_name}"
    