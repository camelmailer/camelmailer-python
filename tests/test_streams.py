from __future__ import annotations

import httpx
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, last_request_json

STREAMS = f"{BASE_URL}/api/v2/server/streams"


@respx.mock
def test_list(client: camelmailer.CamelMailer) -> None:
    respx.get(STREAMS).mock(
        return_value=httpx.Response(200, json=envelope({"streams": [{"permalink": "default"}]}))
    )
    assert client.streams.list() == {"streams": [{"permalink": "default"}]}


@respx.mock
def test_create(client: camelmailer.CamelMailer) -> None:
    route = respx.post(STREAMS).mock(
        return_value=httpx.Response(201, json=envelope({"stream": {"permalink": "broadcasts"}}))
    )
    result = client.streams.create({"name": "Broadcasts", "stream_type": "broadcast"})
    assert result["stream"]["permalink"] == "broadcasts"
    assert last_request_json(route) == {"name": "Broadcasts", "stream_type": "broadcast"}


@respx.mock
def test_get(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{STREAMS}/default").mock(
        return_value=httpx.Response(200, json=envelope({"stream": {"permalink": "default"}}))
    )
    assert client.streams.get("default") == {"stream": {"permalink": "default"}}


@respx.mock
def test_update(client: camelmailer.CamelMailer) -> None:
    route = respx.patch(f"{STREAMS}/default").mock(
        return_value=httpx.Response(200, json=envelope({"stream": {"name": "Renamed"}}))
    )
    result = client.streams.update("default", {"name": "Renamed"})
    assert result["stream"]["name"] == "Renamed"
    assert last_request_json(route) == {"name": "Renamed"}


@respx.mock
def test_archive(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{STREAMS}/old/archive").mock(
        return_value=httpx.Response(200, json=envelope({"archived": True}))
    )
    assert client.streams.archive("old") == {"archived": True}
    assert route.called


@respx.mock
async def test_async_list(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(STREAMS).mock(return_value=httpx.Response(200, json=envelope({"streams": []})))
    assert await aclient.streams.list() == {"streams": []}


@respx.mock
async def test_async_create(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(STREAMS).mock(
        return_value=httpx.Response(201, json=envelope({"stream": {}}))
    )
    await aclient.streams.create({"name": "S"})
    assert last_request_json(route) == {"name": "S"}


@respx.mock
async def test_async_get(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{STREAMS}/s").mock(
        return_value=httpx.Response(200, json=envelope({"stream": {"permalink": "s"}}))
    )
    assert await aclient.streams.get("s") == {"stream": {"permalink": "s"}}


@respx.mock
async def test_async_update(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.patch(f"{STREAMS}/s").mock(
        return_value=httpx.Response(200, json=envelope({"stream": {}}))
    )
    await aclient.streams.update("s", {"name": "N"})
    assert last_request_json(route) == {"name": "N"}


@respx.mock
async def test_async_archive(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(f"{STREAMS}/s/archive").mock(
        return_value=httpx.Response(200, json=envelope({"archived": True}))
    )
    await aclient.streams.archive("s")
    assert route.called
