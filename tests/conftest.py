from pytest_factoryboy import register

from tests.factories import AdFactory, UserFactory

pytests_plugins = "tests.fixtures"

register(AdFactory)
register(UserFactory)
