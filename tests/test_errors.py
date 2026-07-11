from __future__ import annotations

import httpx
import pytest
import respx

import camelmailer
from camelmailer.exceptions import (
    AuthenticationError,
    CamelMailerError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from conftest import BASE_URL
from helpers import error_envelope

PING = f"{BASE_URL}/api/v2/server/ping"
MESSAGES = f"{BASE_URL}/api/v2/server/messages"


@respx.mock
def test_unauthorized_raises_authentication_error(client: camelmailer.CamelMailer) -> None:
    respx.get(PING).mock(
        return_value=httpx.Response(401, json=error_envelope("Unauthorized", "Invalid API key"))
    )
    with pytest.raises(AuthenticationError) as excinfo:
        client.ping()
    assert excinfo.value.code == "Unauthorized"
    assert excinfo.value.message == "Invalid API key"
    assert excinfo.value.status_code == 401


@respx.mock
def test_not_found_raises_not_found_error(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{MESSAGES}/42").mock(
        return_value=httpx.Response(404, json=error_envelope("NotFound", "No such message"))
    )
    with pytest.raises(NotFoundError) as excinfo:
        client.emails.get(42)
    assert excinfo.value.code == "NotFound"
    assert excinfo.value.status_code == 404


@respx.mock
def test_validation_error(client: camelmailer.CamelMailer) -> None:
    respx.post(MESSAGES).mock(
        return_value=httpx.Response(
            422, json=error_envelope("ValidationError", "from domain is not verified")
        )
    )
    with pytest.raises(ValidationError) as excinfo:
        client.emails.send({"from": "a@unverified.test", "to": ["b@example.com"]})
    assert excinfo.value.code == "ValidationError"
    assert "not verified" in excinfo.value.message


@respx.mock
def test_parameter_missing_maps_to_validation_error(client: camelmailer.CamelMailer) -> None:
    respx.post(MESSAGES).mock(
        return_value=httpx.Response(422, json=error_envelope("ParameterMissing", "to is missing"))
    )
    with pytest.raises(ValidationError) as excinfo:
        client.emails.send({"from": "a@b.test"})
    assert excinfo.value.code == "ParameterMissing"


@respx.mock
def test_rate_limit_by_status_code(client: camelmailer.CamelMailer) -> None:
    respx.get(PING).mock(
        return_value=httpx.Response(429, json=error_envelope("SomeNewCode", "Slow down"))
    )
    with pytest.raises(RateLimitError):
        client.ping()


@respx.mock
def test_unknown_code_falls_back_to_base_error(client: camelmailer.CamelMailer) -> None:
    respx.get(PING).mock(
        return_value=httpx.Response(
            403, json=error_envelope("BillingDisabled", "Billing is disabled")
        )
    )
    with pytest.raises(CamelMailerError) as excinfo:
        client.ping()
    assert type(excinfo.value) is CamelMailerError
    assert excinfo.value.code == "BillingDisabled"
    assert excinfo.value.status_code == 403


@respx.mock
def test_error_envelope_wins_even_with_http_200(client: camelmailer.CamelMailer) -> None:
    respx.get(PING).mock(return_value=httpx.Response(200, json=error_envelope("NotFound", "gone")))
    with pytest.raises(NotFoundError):
        client.ping()


@respx.mock
def test_non_json_error_response(client: camelmailer.CamelMailer) -> None:
    respx.get(PING).mock(return_value=httpx.Response(502, text="Bad Gateway"))
    with pytest.raises(CamelMailerError) as excinfo:
        client.ping()
    assert excinfo.value.status_code == 502
    assert excinfo.value.code is None


@respx.mock
def test_non_envelope_json_response(client: camelmailer.CamelMailer) -> None:
    respx.get(PING).mock(return_value=httpx.Response(200, json=[1, 2, 3]))
    with pytest.raises(CamelMailerError, match="envelope"):
        client.ping()


def test_exception_repr_and_str() -> None:
    error = ValidationError("bad input", code="ValidationError", status_code=422)
    assert str(error) == "bad input"
    assert "ValidationError" in repr(error)
    assert "422" in repr(error)
    assert isinstance(error, CamelMailerError)


@respx.mock
async def test_async_authentication_error(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(PING).mock(
        return_value=httpx.Response(401, json=error_envelope("Unauthorized", "Invalid API key"))
    )
    with pytest.raises(AuthenticationError) as excinfo:
        await aclient.ping()
    assert excinfo.value.status_code == 401


@respx.mock
async def test_async_validation_error(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.post(MESSAGES).mock(
        return_value=httpx.Response(422, json=error_envelope("ValidationError", "nope"))
    )
    with pytest.raises(ValidationError):
        await aclient.emails.send({"from": "a@b.test", "to": ["c@d.test"]})


@respx.mock
async def test_async_non_json_error(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(PING).mock(return_value=httpx.Response(500, text="boom"))
    with pytest.raises(CamelMailerError) as excinfo:
        await aclient.ping()
    assert excinfo.value.status_code == 500
