from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope, error_envelope, last_request_json

LAYOUTS = f"{BASE_URL}/api/v2/server/layouts"
LAYOUT = {
    "id": 1,
    "name": "Default",
    "permalink": "default",
    "html_wrapper": "<html><body>{{{ content }}}</body></html>",
}


@respx.mock
def test_crud(client: camelmailer.CamelMailer) -> None:
    respx.get(LAYOUTS).mock(return_value=httpx.Response(200, json=envelope({"layouts": [LAYOUT]})))
    respx.post(LAYOUTS).mock(return_value=httpx.Response(201, json=envelope({"layout": LAYOUT})))
    respx.get(f"{LAYOUTS}/default").mock(
        return_value=httpx.Response(200, json=envelope({"layout": LAYOUT}))
    )
    respx.patch(f"{LAYOUTS}/default").mock(
        return_value=httpx.Response(200, json=envelope({"layout": {**LAYOUT, "name": "Renamed"}}))
    )
    respx.delete(f"{LAYOUTS}/default").mock(
        return_value=httpx.Response(200, json=envelope({"deleted": True}))
    )

    assert len(client.layouts.list()["layouts"]) == 1
    assert (
        client.layouts.create(
            {"name": "Default", "html_wrapper": "<html><body>{{{ content }}}</body></html>"}
        )["layout"]["permalink"]
        == "default"
    )
    assert client.layouts.get("default")["layout"]["id"] == 1
    assert client.layouts.update("default", {"name": "Renamed"})["layout"]["name"] == "Renamed"
    assert client.layouts.delete("default")["deleted"] is True


@respx.mock
def test_a_wrapper_that_escapes_the_body_is_refused(client: camelmailer.CamelMailer) -> None:
    respx.post(LAYOUTS).mock(
        return_value=httpx.Response(
            422,
            json=error_envelope(
                "ValidationError",
                "html_wrapper must embed the body with {{{ content }}} (raw interpolation)",
            ),
        )
    )
    with pytest.raises(camelmailer.ValidationError) as excinfo:
        client.layouts.create({"name": "Broken", "html_wrapper": "{{ content }}"})
    assert "{{{ content }}}" in str(excinfo.value)


@respx.mock
def test_upload_logo_posts_a_data_url(client: camelmailer.CamelMailer) -> None:
    route = respx.post(f"{LAYOUTS}/default/logo").mock(
        return_value=httpx.Response(
            200, json=envelope({"url": "https://mailer.test/assets/layouts/u-1/logo"})
        )
    )
    data_url = "data:image/png;base64,iVBORw0KGgo="
    result = client.layouts.upload_logo("default", data_url)
    assert last_request_json(route) == {"data_url": data_url}
    assert "/assets/layouts/" in result["url"]
