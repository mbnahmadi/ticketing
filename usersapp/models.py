from django.db import models
from django .contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


class UserModel(AbstractUser):
    class GnderChoices(models.TextChoices):
        MALE = "m", "male"
        FEMALE = "f", "female"
    phone_number = models.CharField(null=False, blank=False, validators=[MinLengthValidator(11),MaxLengthValidator(11)])
    gender = models.CharField(max_length=10, choices=GnderChoices.choices, null=False, blank=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.username}- {self.first_name} {self.last_name}"
    