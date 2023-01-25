from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=100, null=False, validators=[MinLengthValidator(10)])
    slug = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1000, null=False)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='image_ad/', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name

    @property
    def username(self):
        return self.author.username if self.author else None


class Selection(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)
