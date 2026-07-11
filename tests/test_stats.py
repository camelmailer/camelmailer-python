from __future__ import annotations

from datetime import datetime, timezone

import httpx
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope

STATS = f"{BASE_URL}/api/v2/server/stats"

COUNTERS = {"total": 10, "outgoing": 9, "sent": 8, "bounced": 1, "opens": 4}


@respx.mock
def test_get(client: camelmailer.CamelMailer) -> None:
    respx.get(STATS).mock(return_value=httpx.Response(200, json=envelope({"stats": COUNTERS})))
    stats = client.stats.get()
    assert stats["total"] == 10
    assert stats["sent"] == 8


@respx.mock
def test_get_with_datetime_window(client: camelmailer.CamelMailer) -> None:
    route = respx.get(STATS).mock(
        return_value=httpx.Response(200, json=envelope({"stats": COUNTERS}))
    )
    client.stats.get(
        from_=datetime(2026, 1, 1, tzinfo=timezone.utc),
        to="2026-02-01T00:00:00Z",
    )
    params = dict(route.calls.last.request.url.params)
    assert params["from"] == "2026-01-01T00:00:00+00:00"
    assert params["to"] == "2026-02-01T00:00:00Z"


@respx.mock
def test_deliveries(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{STATS}/deliveries").mock(
        return_value=httpx.Response(200, json=envelope({"queued": 3, "delivered_24h": 100}))
    )
    assert client.stats.deliveries() == {"queued": 3, "delivered_24h": 100}


@respx.mock
async def test_async_get(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.get(STATS).mock(
        return_value=httpx.Response(200, json=envelope({"stats": COUNTERS}))
    )
    stats = await aclient.stats.get(from_="2026-01-01T00:00:00Z")
    assert stats["total"] == 10
    assert dict(route.calls.last.request.url.params)["from"] == "2026-01-01T00:00:00Z"


@respx.mock
async def test_async_deliveries(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{STATS}/deliveries").mock(
        return_value=httpx.Response(200, json=envelope({"queued": 0}))
    )
    assert await aclient.stats.deliveries() == {"queued": 0}
