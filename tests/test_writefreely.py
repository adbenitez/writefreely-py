import pytest

import writefreely as wf


def test_account(requests_mock) -> None:
    client = wf.client(token="test-token1")
    assert client.token == "test-token1"

    client = wf.client()
    assert client.host == "https://write.as"
    assert client.token is None
    assert not client.is_authenticated()
    requests_mock.post(
        "https://write.as/api/auth/login",
        json={"data": {"access_token": "test-token2"}},
    )
    client.login("test-user2", "test-password2")
    assert client.token == "test-token2"
    assert client.is_authenticated()

    requests_mock.post(
        "https://example.com/api/auth/login",
        json={"data": {"access_token": "test-token3"}},
    )
    client = wf.client(
        host="https://example.com", user="test-user3", password="test-password3"
    )
    assert client.host == "https://example.com"
    assert client.token == "test-token3"

    requests_mock.get("https://example.com/api/me", json={"data": "test-data"})
    assert client.me() == "test-data"

    requests_mock.delete("https://example.com/api/auth/me")
    client.logout()
    assert client.token is None
    assert not client.is_authenticated()


def test_posts(requests_mock) -> None:
    client = wf.client(token="test-token")

    requests_mock.post("https://write.as/api/posts", json={"data": "test-data1"})
    post = client.create_post(title="Hello World!", body="test body")
    assert post == "test-data1"

    requests_mock.get("https://write.as/api/posts/1234", json={"data": "test-data2"})
    post = client.get_post("1234")
    assert post == "test-data2"

    requests_mock.get("https://write.as/api/me/posts", json={"data": "test-data3"})
    assert client.get_posts() == "test-data3"


def test_collections(requests_mock) -> None:
    client = wf.client(token="test-token")

    requests_mock.post("https://write.as/api/collections", json={"data": "test-data1"})
    assert client.create_collection(alias="test-alias") == "test-data1"

    requests_mock.get(
        "https://write.as/api/collections/test-alias", json={"data": "test-data2"}
    )
    assert client.get_collection(alias="test-alias") == "test-data2"

    requests_mock.get(
        "https://write.as/api/me/collections", json={"data": "test-data3"}
    )
    assert client.get_collections() == "test-data3"
