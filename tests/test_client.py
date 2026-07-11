from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from conftest import API_KEY, BASE_URL
from helpers import envelope


def test_missing_api_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(camelmailer.API_KEY_ENV, raising=False)
    with pytest.raises(ValueError, match="CAMELMAILER_API_KEY"):
        camelmailer.CamelMailer()


def test_missing_api_key_raises_async(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(camelmailer.API_KEY_ENV, raising=False)
    with pytest.raises(ValueError, match="CAMELMAILER_API_KEY"):
        camelmailer.AsyncCamelMailer()


def test_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(camelmailer.API_KEY_ENV, "cm_env_key")
    with respx.mock, camelmailer.CamelMailer(base_url=BASE_URL) as client:
        route = respx.get(f"{BASE_URL}/api/v2/server/ping").mock(
            return_value=httpx.Response(200, json=envelope({"pong": True}))
        )
        client.ping()
    assert route.calls.last.request.headers["X-Server-API-Key"] == "cm_env_key"


def test_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(camelmailer.BASE_URL_ENV, "https://env.mailer.test/")
    client = camelmailer.CamelMailer(api_key=API_KEY)
    assert client.base_url == "https://env.mailer.test"
    client.close()


def test_default_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(camelmailer.BASE_URL_ENV, raising=False)
    with camelmailer.CamelMailer(api_key=API_KEY) as client:
        assert client.base_url == "https://app.camelmailer.com"


@respx.mock
def test_base_url_override_is_used(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{BASE_URL}/api/v2/server/ping").mock(
        return_value=httpx.Response(200, json=envelope({"pong": True}))
    )
    client.ping()
    assert route.called
    assert str(route.calls.last.request.url).startswith(BASE_URL)


@respx.mock
def test_api_key_and_user_agent_headers(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{BASE_URL}/api/v2/server/ping").mock(
        return_value=httpx.Response(200, json=envelope({}))
    )
    client.ping()
    request = respx.calls.last.request
    assert request.headers["X-Server-API-Key"] == API_KEY
    assert request.headers["User-Agent"] == f"camelmailer-python/{camelmailer.__version__}"


@respx.mock
def test_server(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{BASE_URL}/api/v2/server/").mock(
        return_value=httpx.Response(200, json=envelope({"server": {"name": "prod"}}))
    )
    assert client.server() == {"server": {"name": "prod"}}
    assert route.called


@respx.mock
def test_custom_http_client_is_not_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    http_client = httpx.Client()
    client = camelmailer.CamelMailer(api_key=API_KEY, base_url=BASE_URL, http_client=http_client)
    respx.get(f"{BASE_URL}/api/v2/server/ping").mock(
        return_value=httpx.Response(200, json=envelope({}))
    )
    client.ping()
    client.close()
    assert not http_client.is_closed
    http_client.close()


@respx.mock
async def test_async_ping(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.get(f"{BASE_URL}/api/v2/server/ping").mock(
        return_value=httpx.Response(200, json=envelope({"pong": True}))
    )
    assert await aclient.ping() == {"pong": True}
    assert route.calls.last.request.headers["X-Server-API-Key"] == API_KEY


@respx.mock
async def test_async_server_and_context_manager() -> None:
    respx.get(f"{BASE_URL}/api/v2/server/").mock(
        return_value=httpx.Response(200, json=envelope({"server": {}}))
    )
    async with camelmailer.AsyncCamelMailer(api_key=API_KEY, base_url=BASE_URL) as client:
        assert await client.server() == {"server": {}}
