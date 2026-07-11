from __future__ import annotations

import httpx
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, last_request_json

MESSAGES = f"{BASE_URL}/api/v2/server/messages"

SEND_RESULT = {
    "message_id": 1234,
    "recipients": [{"rcpt_to": "ada@example.com", "status": "queued", "token": "tok_1"}],
}


@respx.mock
def test_send(client: camelmailer.CamelMailer) -> None:
    route = respx.post(MESSAGES).mock(return_value=httpx.Response(201, json=envelope(SEND_RESULT)))
    result = client.emails.send(
        {
            "from": "billing@acme.com",
            "to": ["ada@example.com"],
            "subject": "Your receipt",
            "text_body": "Thanks!",
            "tag": "receipt",
        }
    )
    assert result["message_id"] == 1234
    assert result["recipients"][0]["status"] == "queued"
    body = last_request_json(route)
    assert body["from"] == "billing@acme.com"
    assert body["to"] == ["ada@example.com"]
    assert body["tag"] == "receipt"


@respx.mock
def test_send_with_attachment_and_named_address(client: camelmailer.CamelMailer) -> None:
    route = respx.post(MESSAGES).mock(return_value=httpx.Response(201, json=envelope(SEND_RESULT)))
    client.emails.send(
        {
            "from": {"email": "billing@acme.com", "name": "Acme Billing"},
            "to": ["ada@example.com"],
            "subject": "Invoice",
            "html_body": "<p>Hi</p>",
            "attachments": [
                {"name": "invoice.pdf", "content_type": "application/pdf", "data_base64": "aGk="}
            ],
        }
    )
    body = last_request_json(route)
    assert body["from"] == {"email": "billing@acme.com", "name": "Acme Billing"}
    assert body["attachments"][0]["name"] == "invoice.pdf"


@respx.mock
def test_send_batch(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/batch").mock(
        return_value=httpx.Response(200, json=envelope({"results": [SEND_RESULT]}))
    )
    result = client.emails.send_batch(
        [{"from": "a@acme.com", "to": ["b@example.com"], "subject": "Hi", "text_body": "Yo"}]
    )
    assert result == {"results": [SEND_RESULT]}
    assert last_request_json(route)["messages"][0]["from"] == "a@acme.com"


@respx.mock
def test_send_with_template(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/with_template").mock(
        return_value=httpx.Response(201, json=envelope(SEND_RESULT))
    )
    result = client.emails.send_with_template(
        {
            "from": "hello@acme.com",
            "to": ["ada@example.com"],
            "template": "welcome",
            "template_model": {"name": "Ada"},
        }
    )
    assert result["message_id"] == 1234
    body = last_request_json(route)
    assert body["template"] == "welcome"
    assert body["template_model"] == {"name": "Ada"}


@respx.mock
def test_send_with_template_batch(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/with_template/batch").mock(
        return_value=httpx.Response(200, json=envelope({"results": []}))
    )
    client.emails.send_with_template_batch(
        [{"from": "hello@acme.com", "to": ["ada@example.com"], "template": "welcome"}]
    )
    assert last_request_json(route)["messages"][0]["template"] == "welcome"


@respx.mock
def test_get(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{MESSAGES}/77").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 77, "subject": "Hi"}}))
    )
    assert client.emails.get(77) == {"message": {"id": 77, "subject": "Hi"}}


@respx.mock
def test_list_with_filters(client: camelmailer.CamelMailer) -> None:
    route = respx.get(MESSAGES).mock(
        return_value=httpx.Response(
            200,
            json=envelope(
                {
                    "messages": [{"id": 1, "rcpt_to": "ada@example.com"}],
                    "pagination": {"page": 2, "per_page": 50, "total": 51, "total_pages": 2},
                }
            ),
        )
    )
    result = client.emails.list(page=2, per_page=50, scope="outgoing", tag="receipt", query="ada")
    assert result["messages"][0]["id"] == 1
    assert result["pagination"]["total_pages"] == 2
    params = dict(route.calls.last.request.url.params)
    assert params == {
        "page": "2",
        "per_page": "50",
        "scope": "outgoing",
        "tag": "receipt",
        "query": "ada",
    }


@respx.mock
def test_list_without_filters_sends_no_params(client: camelmailer.CamelMailer) -> None:
    route = respx.get(MESSAGES).mock(
        return_value=httpx.Response(200, json=envelope({"messages": [], "pagination": {}}))
    )
    client.emails.list()
    assert str(route.calls.last.request.url) == MESSAGES


@respx.mock
def test_deliveries(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/deliveries").mock(
        return_value=httpx.Response(200, json=envelope({"deliveries": [{"status": "Sent"}]}))
    )
    assert client.emails.deliveries(9) == {"deliveries": [{"status": "Sent"}]}


@respx.mock
def test_opens(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/opens").mock(
        return_value=httpx.Response(200, json=envelope({"opens": []}))
    )
    assert client.emails.opens(9) == {"opens": []}


@respx.mock
def test_clicks(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/clicks").mock(
        return_value=httpx.Response(200, json=envelope({"clicks": []}))
    )
    assert client.emails.clicks(9) == {"clicks": []}


@respx.mock
def test_raw(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/raw").mock(
        return_value=httpx.Response(200, json=envelope({"raw": "From: a@b.c\r\n..."}))
    )
    assert client.emails.raw(9)["raw"].startswith("From:")


@respx.mock
async def test_async_send(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(MESSAGES).mock(return_value=httpx.Response(201, json=envelope(SEND_RESULT)))
    result = await aclient.emails.send(
        {"from": "billing@acme.com", "to": ["ada@example.com"], "subject": "Hi"}
    )
    assert result["message_id"] == 1234
    assert last_request_json(route)["from"] == "billing@acme.com"


@respx.mock
async def test_async_send_batch(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/batch").mock(
        return_value=httpx.Response(200, json=envelope({"results": []}))
    )
    await aclient.emails.send_batch([{"from": "a@acme.com", "to": ["b@example.com"]}])
    assert "messages" in last_request_json(route)


@respx.mock
async def test_async_send_with_template(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/with_template").mock(
        return_value=httpx.Response(201, json=envelope(SEND_RESULT))
    )
    await aclient.emails.send_with_template(
        {"from": "a@acme.com", "to": ["b@example.com"], "template": "welcome"}
    )
    assert last_request_json(route)["template"] == "welcome"


@respx.mock
async def test_async_send_with_template_batch(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(f"{MESSAGES}/with_template/batch").mock(
        return_value=httpx.Response(200, json=envelope({"results": []}))
    )
    await aclient.emails.send_with_template_batch(
        [{"from": "a@acme.com", "to": ["b@example.com"], "template": "welcome"}]
    )
    assert route.called


@respx.mock
async def test_async_get(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{MESSAGES}/5").mock(
        return_value=httpx.Response(200, json=envelope({"message": {"id": 5}}))
    )
    assert await aclient.emails.get(5) == {"message": {"id": 5}}


@respx.mock
async def test_async_list(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.get(MESSAGES).mock(
        return_value=httpx.Response(200, json=envelope({"messages": [], "pagination": {}}))
    )
    result = await aclient.emails.list(scope="incoming", stream="broadcasts")
    assert result["messages"] == []
    params = dict(route.calls.last.request.url.params)
    assert params == {"scope": "incoming", "stream": "broadcasts"}


@respx.mock
async def test_async_deliveries(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/deliveries").mock(
        return_value=httpx.Response(200, json=envelope({"deliveries": []}))
    )
    assert await aclient.emails.deliveries(9) == {"deliveries": []}


@respx.mock
async def test_async_opens(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/opens").mock(
        return_value=httpx.Response(200, json=envelope({"opens": []}))
    )
    assert await aclient.emails.opens(9) == {"opens": []}


@respx.mock
async def test_async_clicks(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/clicks").mock(
        return_value=httpx.Response(200, json=envelope({"clicks": []}))
    )
    assert await aclient.emails.clicks(9) == {"clicks": []}


@respx.mock
async def test_async_raw(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{MESSAGES}/9/raw").mock(
        return_value=httpx.Response(200, json=envelope({"raw": "From: x"}))
    )
    assert await aclient.emails.raw(9) == {"raw": "From: x"}
