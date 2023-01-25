import pytest

from tests.factories import AdFactory, UserFactory


@pytest.mark.django_db
def test_create_selection(client, auth_token):
    ads = AdFactory.create_batch(5)
    owner = UserFactory.create()

    data = {
        "name": "test",
        "owner": owner,
        "items": ads,
    }

    expected_response = {
        "name": "test",
        "owner": owner.pk,
        "items": [ad.pk for ad in ads],
    }

    response = client.post(
        "/selection/create/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer" + auth_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
