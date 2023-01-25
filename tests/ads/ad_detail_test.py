import pytest


@pytest.mark.django_db
def test_retrieve_vacancy(client, ad, auth_token):
    expected_response = {
        "id": ad.pk,
        "name": "test",
        "slug": "test",
        "author": ad.author_id,
        "price": 100,
        "description": "test description",
        "is_published": False,
        "image": None,
        "category": None,
    }

    response = client.get(
        f"/ad/{ad.pk}/",
        HTTP_AUTHORIZATION="Bearer" + auth_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
