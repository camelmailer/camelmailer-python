from __future__ import annotations

import httpx
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope

BOUNCES = f"{BASE_URL}/api/v2/server/bounces"


@respx.mock
def test_list(client: camelmailer.CamelMailer) -> None:
    route = respx.get(BOUNCES).mock(
        return_value=httpx.Response(
            200, json=envelope({"messages": [{"id": 3, "bounce": True}], "pagination": {}})
        )
    )
    result = client.bounces.list(page=1, per_page=25)
    assert result["messages"][0]["bounce"] is True
    assert dict(route.calls.last.request.url.params) == {"page": "1", "per_page": "25"}


@respx.mock
def test_get(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{BOUNCES}/3").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 3}}))
    )
    assert client.bounces.get(3) == {"message": {"id": 3}}


@respx.mock
async def test_async_list(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(BOUNCES).mock(return_value=httpx.Response(200, json=envelope({"messages": []})))
    assert await aclient.bounces.list() == {"messages": []}


@respx.mock
async def test_async_get(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{BOUNCES}/4").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 4}}))
    )
    assert await aclient.bounces.get(4) == {"message": {"id": 4}}
