from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, error_envelope, last_request_json

MESSAGES = f"{BASE_URL}/api/v2/server/messages"
SEND = {"from": "billing@acme.com", "to": ["ada@example.com"], "subject": "Receipt"}


@respx.mock
def test_the_key_travels_as_a_header_not_in_the_body(client: camelmailer.CamelMailer) -> None:
    route = respx.post(MESSAGES).mock(
        return_value=httpx.Response(200, json=envelope({"message_id": 1}))
    )
    client.emails.send(SEND, idempotency_key="order-4711")
    assert route.calls.last.request.headers["Idempotency-Key"] == "order-4711"
    # The body is what the server hashes for the claim, so the key must not
    # end up inside it.
    assert last_request_json(route) == SEND


@respx.mock
def test_no_header_without_a_key(client: camelmailer.CamelMailer) -> None:
    route = respx.post(MESSAGES).mock(
        return_value=httpx.Response(200, json=envelope({"message_id": 1}))
    )
    client.emails.send(SEND)
    assert "Idempotency-Key" not in route.calls.last.request.headers


@respx.mock
def test_batch_sends_a_bare_array(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/batch").mock(
        return_value=httpx.Response(200, json=envelope({"messages": []}))
    )
    client.emails.send_batch([SEND], idempotency_key="nightly")
    # The endpoint deserializes into Vec<SendMessage>; a {"messages": [...]}
    # wrapper is rejected with "invalid type: map, expected a sequence".
    assert last_request_json(route) == [SEND]
    assert route.calls.last.request.headers["Idempotency-Key"] == "nightly"


@respx.mock
def test_template_batch_sends_a_bare_array_too(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/with_template/batch").mock(
        return_value=httpx.Response(200, json=envelope({"messages": []}))
    )
    client.emails.send_with_template_batch([{"template": "welcome", "to": ["a@b.test"]}])
    assert isinstance(last_request_json(route), list)


@respx.mock
def test_a_reused_key_with_different_content_raises(client: camelmailer.CamelMailer) -> None:
    respx.post(MESSAGES).mock(
        return_value=httpx.Response(
            409,
            json=error_envelope(
                "InvalidIdempotentRequest", "The key was used for a different request"
            ),
        )
    )
    with pytest.raises(camelmailer.ValidationError):
        client.emails.send(SEND, idempotency_key="order-4711")


@respx.mock
def test_a_spent_send_allowance_raises_its_own_class(client: camelmailer.CamelMailer) -> None:
    respx.post(MESSAGES).mock(
        return_value=httpx.Response(
            429,
            json=error_envelope("SendLimitExceeded", "The server reached its 30-day send limit"),
        )
    )
    with pytest.raises(camelmailer.SendLimitExceededError) as excinfo:
        client.emails.send(SEND)
    # It is still a RateLimitError, so code that already catches that keeps
    # working.
    assert isinstance(excinfo.value, camelmailer.RateLimitError)


@respx.mock
def test_send_to_stream_reports_queued_against_skipped(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{BASE_URL}/api/v2/server/streams/product-news/send").mock(
        return_value=httpx.Response(200, json=envelope({"queued": 1000, "skipped": 240}))
    )
    result = client.emails.send_to_stream("product-news", {"subject": "Hi", "text_body": "Hello"})
    assert result == {"queued": 1000, "skipped": 240}
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_async_send_carries_the_key(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(MESSAGES).mock(
        return_value=httpx.Response(200, json=envelope({"message_id": 1}))
    )
    await aclient.emails.send(SEND, idempotency_key="k")
    assert route.calls.last.request.headers["Idempotency-Key"] == "k"
