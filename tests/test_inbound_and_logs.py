from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope

SERVER = f"{BASE_URL}/api/v2/server"


@respx.mock
def test_inbound_list_sends_only_the_given_filters(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{SERVER}/inbound").mock(
        return_value=httpx.Response(200, json=envelope({"inbound": [], "pagination": {}}))
    )
    client.inbound.list(stream="support-inbox", status="Held")
    query = route.calls.last.request.url.params
    assert query["stream"] == "support-inbox"
    assert query["status"] == "Held"
    # Filters that were not given must not appear at all; an empty tag= would
    # match differently than no tag.
    assert "tag" not in query


@respx.mock
def test_inbound_retry_and_bypass(client: camelmailer.CamelMailer) -> None:
    respx.post(f"{SERVER}/inbound/55/retry").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 55}, "requeued": True}))
    )
    respx.post(f"{SERVER}/inbound/55/bypass").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 55}, "requeued": True}))
    )
    assert client.inbound.retry(55)["requeued"] is True
    assert client.inbound.bypass(55)["requeued"] is True


@respx.mock
def test_logs_list_maps_from_underscore_to_from(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{SERVER}/logs").mock(
        return_value=httpx.Response(200, json=envelope({"requests": [], "pagination": {}}))
    )
    client.logs.list(status="4xx", method="POST", from_="2026-09-01T00:00:00Z")
    query = route.calls.last.request.url.params
    assert query["status"] == "4xx"
    # `from` is a Python keyword, so the argument carries an underscore and
    # has to reach the wire without it.
    assert query["from"] == "2026-09-01T00:00:00Z"
    assert "from_" not in query


@respx.mock
def test_tags(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{SERVER}/tags").mock(
        return_value=httpx.Response(200, json=envelope({"tags": [{"tag": "receipt", "count": 91}]}))
    )
    assert client.logs.tags()["tags"][0]["count"] == 91


@respx.mock
@pytest.mark.asyncio
async def test_async_inbound(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{SERVER}/inbound/55").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 55}}))
    )
    assert (await aclient.inbound.get(55))["message"]["id"] == 55
