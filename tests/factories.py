import factory

from ads.models import Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "123qwer"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "test"
    slug = "test"
    author = factory.SubFactory(UserFactory)
    price = 100
    description = "test description"
