from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class User(models.Model):
    ROLE = [
        ("member", "Участник"),
        ("moderator", "Модератор"),
        ("admin", "Админ"),
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=9, choices=ROLE)
    age = models.SmallIntegerField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
