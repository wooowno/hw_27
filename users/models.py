from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def date_birth_check(value):
    user_age = relativedelta(value, date.today()).years
    if user_age < 9:
        raise ValidationError("Access forbidden.")


def email_check(value):
    if "rambler.ru" in value:
        raise ValidationError(f"Email's domain is rambler.")


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLE = [
        (MEMBER, MEMBER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    role = models.CharField(max_length=9, choices=ROLE)
    age = models.SmallIntegerField()
    locations = models.ManyToManyField(Location)
    date_birth = models.DateField(validators=[date_birth_check])
    email = models.EmailField(unique=True, validators=[email_check])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
