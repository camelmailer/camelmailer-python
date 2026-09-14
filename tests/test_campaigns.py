from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, error_envelope, last_request_json

SERVER = f"{BASE_URL}/api/v2/server"
CAMPAIGN = {
    "id": 7,
    "stream_id": 2,
    "name": "September newsletter",
    "status": "draft",
    "scheduled_at": None,
    "stream": {"permalink": "product-news", "name": "Product news"},
}


@respx.mock
def test_list_carries_the_stream_inline(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{SERVER}/campaigns").mock(
        return_value=httpx.Response(200, json=envelope({"campaigns": [CAMPAIGN]}))
    )
    result = client.campaigns.list()
    assert result["campaigns"][0]["stream"]["permalink"] == "product-news"


@respx.mock
def test_list_for_stream(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{SERVER}/streams/product-news/campaigns").mock(
        return_value=httpx.Response(200, json=envelope({"campaigns": []}))
    )
    client.campaigns.list_for_stream("product-news")
    assert route.called


@respx.mock
def test_get_returns_stats_alongside(client: camelmailer.CamelMailer) -> None:
    stats = {
        "total": 120,
        "sent": 120,
        "delivered": 118,
        "failed": 2,
        "opened": 61,
        "clicked": 12,
        "unsubscribed": 1,
    }
    respx.get(f"{SERVER}/campaigns/7").mock(
        return_value=httpx.Response(200, json=envelope({"campaign": CAMPAIGN, "stats": stats}))
    )
    result = client.campaigns.get(7)
    assert result["stats"]["delivered"] == 118


@respx.mock
def test_create_draft_names_its_stream_in_the_body(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{SERVER}/campaigns").mock(
        return_value=httpx.Response(201, json=envelope({"campaign": CAMPAIGN}))
    )
    result = client.campaigns.create_draft(
        {"stream": "product-news", "name": "September newsletter", "from": "news@acme.com"}
    )
    assert result["campaign"]["status"] == "draft"
    # `from` is the API field. A `from_address` key reaches the server
    # untranslated and the create is refused for a missing From address.
    assert last_request_json(route) == {
        "stream": "product-news",
        "name": "September newsletter",
        "from": "news@acme.com",
    }


@respx.mock
def test_create_draft_arms_a_schedule(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{SERVER}/campaigns").mock(
        return_value=httpx.Response(
            201, json=envelope({"campaign": {**CAMPAIGN, "status": "scheduled"}})
        )
    )
    result = client.campaigns.create_draft(
        {"stream": "product-news", "from": "news@acme.com", "scheduled_at": "2026-10-01T08:00:00Z"}
    )
    assert result["campaign"]["status"] == "scheduled"
    assert last_request_json(route)["scheduled_at"] == "2026-10-01T08:00:00Z"


@respx.mock
def test_create_and_send_goes_out_immediately(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{SERVER}/streams/product-news/campaigns").mock(
        return_value=httpx.Response(
            201, json=envelope({"campaign": {**CAMPAIGN, "status": "sending"}})
        )
    )
    result = client.campaigns.create_and_send(
        "product-news", {"name": "September newsletter", "from": "news@acme.com"}
    )
    # The stream-scoped route expands to the subscribers before it answers.
    assert result["campaign"]["status"] == "sending"
    assert last_request_json(route)["from"] == "news@acme.com"


@respx.mock
def test_deprecated_create_still_hits_the_send_route(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{SERVER}/streams/product-news/campaigns").mock(
        return_value=httpx.Response(
            201, json=envelope({"campaign": {**CAMPAIGN, "status": "sending"}})
        )
    )
    client.campaigns.create("product-news", {"name": "September newsletter"})
    assert route.called


@respx.mock
def test_scheduling_sends_the_timestamp(client: camelmailer.CamelMailer) -> None:
    route = respx.patch(f"{SERVER}/campaigns/7").mock(
        return_value=httpx.Response(200, json=envelope({"campaign": CAMPAIGN}))
    )
    client.campaigns.update(7, {"scheduled_at": "2026-10-01T08:00:00Z"})
    assert last_request_json(route) == {"scheduled_at": "2026-10-01T08:00:00Z"}


@respx.mock
def test_an_explicit_none_survives_and_is_what_clears_a_schedule(
    client: camelmailer.CamelMailer,
) -> None:
    route = respx.patch(f"{SERVER}/campaigns/7").mock(
        return_value=httpx.Response(200, json=envelope({"campaign": CAMPAIGN}))
    )
    client.campaigns.update(7, {"scheduled_at": None})
    # None has to reach the wire as null. Dropping it would mean "leave the
    # schedule alone", which is the opposite of what the caller asked for.
    assert last_request_json(route) == {"scheduled_at": None}


@respx.mock
def test_send_and_cancel(client: camelmailer.CamelMailer) -> None:
    send = respx.post(f"{SERVER}/campaigns/7/send").mock(
        return_value=httpx.Response(
            200, json=envelope({"campaign": {**CAMPAIGN, "status": "sending"}})
        )
    )
    cancel = respx.post(f"{SERVER}/campaigns/7/cancel").mock(
        return_value=httpx.Response(
            200, json=envelope({"campaign": {**CAMPAIGN, "status": "canceled"}})
        )
    )
    assert client.campaigns.send(7)["campaign"]["status"] == "sending"
    assert client.campaigns.cancel(7)["campaign"]["status"] == "canceled"
    assert send.called and cancel.called


@respx.mock
def test_sending_a_sent_campaign_raises(client: camelmailer.CamelMailer) -> None:
    respx.post(f"{SERVER}/campaigns/7/send").mock(
        return_value=httpx.Response(
            422, json=error_envelope("ValidationError", "Campaign is already sent")
        )
    )
    with pytest.raises(camelmailer.ValidationError):
        client.campaigns.send(7)


@respx.mock
@pytest.mark.asyncio
async def test_async_mirrors_the_sync_surface(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{SERVER}/campaigns").mock(
        return_value=httpx.Response(200, json=envelope({"campaigns": [CAMPAIGN]}))
    )
    result = await aclient.campaigns.list()
    assert result["campaigns"][0]["id"] == 7

    respx.post(f"{SERVER}/campaigns").mock(
        return_value=httpx.Response(201, json=envelope({"campaign": CAMPAIGN}))
    )
    draft = await aclient.campaigns.create_draft(
        {"stream": "product-news", "from": "news@acme.com"}
    )
    assert draft["campaign"]["status"] == "draft"

    route = respx.post(f"{SERVER}/streams/product-news/campaigns").mock(
        return_value=httpx.Response(
            201, json=envelope({"campaign": {**CAMPAIGN, "status": "sending"}})
        )
    )
    sent = await aclient.campaigns.create_and_send("product-news", {"name": "Now"})
    assert sent["campaign"]["status"] == "sending"

    await aclient.campaigns.create("product-news", {"name": "Now"})
    assert route.call_count == 2
