from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, error_envelope, last_request_json

SUBS = f"{BASE_URL}/api/v2/server/streams/product-news/subscribers"
SUBSCRIBER = {"id": 3, "address": "ada@example.com", "status": "subscribed"}


@respx.mock
def test_list(client: camelmailer.CamelMailer) -> None:
    respx.get(SUBS).mock(
        return_value=httpx.Response(200, json=envelope({"subscribers": [SUBSCRIBER]}))
    )
    assert client.subscribers.list("product-news")["subscribers"][0]["address"] == "ada@example.com"


@respx.mock
def test_add_defaults_the_status_server_side(client: camelmailer.CamelMailer) -> None:
    route = respx.post(SUBS).mock(
        return_value=httpx.Response(201, json=envelope({"subscriber": SUBSCRIBER}))
    )
    result = client.subscribers.add("product-news", {"address": "ada@example.com"})
    assert last_request_json(route) == {"address": "ada@example.com"}
    assert result["subscriber"]["status"] == "subscribed"


@respx.mock
def test_an_invalid_status_raises(client: camelmailer.CamelMailer) -> None:
    respx.post(SUBS).mock(
        return_value=httpx.Response(
            422, json=error_envelope("ValidationError", 'Subscription status "maybe" is not valid')
        )
    )
    with pytest.raises(camelmailer.ValidationError):
        client.subscribers.add("product-news", {"address": "ada@example.com", "status": "maybe"})


@respx.mock
def test_import_reports_added_against_total(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{SUBS}/import").mock(
        return_value=httpx.Response(200, json=envelope({"added": 2, "total": 3}))
    )
    result = client.subscribers.import_(
        "product-news", ["ada@example.com", "grace@example.com", "ada@example.com"]
    )
    assert result == {"added": 2, "total": 3}
    assert last_request_json(route)["addresses"][0] == "ada@example.com"


@respx.mock
def test_remove_encodes_the_address(client: camelmailer.CamelMailer) -> None:
    # A + in an address is significant; unencoded it would arrive as a space.
    route = respx.delete(f"{SUBS}/ada%2Bnews%40example.com").mock(
        return_value=httpx.Response(200, json=envelope({"deleted": True}))
    )
    assert client.subscribers.remove("product-news", "ada+news@example.com")["deleted"] is True
    assert route.called


@respx.mock
def test_complaint_unsubscribes(client: camelmailer.CamelMailer) -> None:
    respx.post(f"{SUBS}/ada%40example.com/complaint").mock(
        return_value=httpx.Response(
            200, json=envelope({"subscriber": {**SUBSCRIBER, "status": "unsubscribed"}})
        )
    )
    result = client.subscribers.complaint("product-news", "ada@example.com")
    assert result["subscriber"]["status"] == "unsubscribed"


@respx.mock
@pytest.mark.asyncio
async def test_async_import(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.post(f"{SUBS}/import").mock(
        return_value=httpx.Response(200, json=envelope({"added": 1, "total": 1}))
    )
    assert (await aclient.subscribers.import_("product-news", ["x@example.com"]))["added"] == 1
