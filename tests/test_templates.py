from __future__ import annotations

import httpx
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, last_request_json

TEMPLATES = f"{BASE_URL}/api/v2/server/templates"


@respx.mock
def test_list(client: camelmailer.CamelMailer) -> None:
    respx.get(TEMPLATES).mock(
        return_value=httpx.Response(200, json=envelope({"templates": [{"name": "welcome"}]}))
    )
    assert client.templates.list() == {"templates": [{"name": "welcome"}]}


@respx.mock
def test_create(client: camelmailer.CamelMailer) -> None:
    route = respx.post(TEMPLATES).mock(
        return_value=httpx.Response(
            201, json=envelope({"template": {"name": "welcome", "permalink": "welcome"}})
        )
    )
    result = client.templates.create(
        {"name": "welcome", "subject": "Hi {{ name }}", "html_body": "<p>Hi {{ name }}</p>"}
    )
    assert result["template"]["permalink"] == "welcome"
    assert last_request_json(route)["subject"] == "Hi {{ name }}"


@respx.mock
def test_get(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{TEMPLATES}/welcome").mock(
        return_value=httpx.Response(200, json=envelope({"template": {"name": "welcome"}}))
    )
    assert client.templates.get("welcome") == {"template": {"name": "welcome"}}


@respx.mock
def test_update(client: camelmailer.CamelMailer) -> None:
    route = respx.patch(f"{TEMPLATES}/welcome").mock(
        return_value=httpx.Response(200, json=envelope({"template": {"name": "welcome v2"}}))
    )
    result = client.templates.update("welcome", {"name": "welcome v2"})
    assert result["template"]["name"] == "welcome v2"
    assert last_request_json(route) == {"name": "welcome v2"}


@respx.mock
def test_archive(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{TEMPLATES}/welcome/archive").mock(
        return_value=httpx.Response(200, json=envelope({"archived": True}))
    )
    assert client.templates.archive("welcome") == {"archived": True}
    assert route.called


@respx.mock
def test_render(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{TEMPLATES}/welcome/render").mock(
        return_value=httpx.Response(
            200, json=envelope({"subject": "Hi Ada", "html_body": "<p>Hi Ada</p>"})
        )
    )
    result = client.templates.render("welcome", {"name": "Ada"})
    assert result["subject"] == "Hi Ada"
    assert last_request_json(route) == {"template_model": {"name": "Ada"}}


@respx.mock
def test_render_without_model(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{TEMPLATES}/welcome/render").mock(
        return_value=httpx.Response(200, json=envelope({"subject": "Hi "}))
    )
    client.templates.render("welcome")
    assert last_request_json(route) == {"template_model": {}}


@respx.mock
async def test_async_list(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(TEMPLATES).mock(return_value=httpx.Response(200, json=envelope({"templates": []})))
    assert await aclient.templates.list() == {"templates": []}


@respx.mock
async def test_async_create(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(TEMPLATES).mock(
        return_value=httpx.Response(201, json=envelope({"template": {"name": "t"}}))
    )
    await aclient.templates.create({"name": "t"})
    assert last_request_json(route) == {"name": "t"}


@respx.mock
async def test_async_get(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{TEMPLATES}/t").mock(
        return_value=httpx.Response(200, json=envelope({"template": {"name": "t"}}))
    )
    assert await aclient.templates.get("t") == {"template": {"name": "t"}}


@respx.mock
async def test_async_update(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.patch(f"{TEMPLATES}/t").mock(
        return_value=httpx.Response(200, json=envelope({"template": {}}))
    )
    await aclient.templates.update("t", {"subject": "s"})
    assert last_request_json(route) == {"subject": "s"}


@respx.mock
async def test_async_archive(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(f"{TEMPLATES}/t/archive").mock(
        return_value=httpx.Response(200, json=envelope({"archived": True}))
    )
    await aclient.templates.archive("t")
    assert route.called


@respx.mock
async def test_async_render(aclient: camelmailer.AsyncCamelMailer) -> None:
    route = respx.post(f"{TEMPLATES}/t/render").mock(
        return_value=httpx.Response(200, json=envelope({"subject": "Hi Ada"}))
    )
    result = await aclient.templates.render("t", {"name": "Ada"})
    assert result["subject"] == "Hi Ada"
    assert last_request_json(route) == {"template_model": {"name": "Ada"}}
