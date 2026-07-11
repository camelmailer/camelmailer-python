"""HTTP transport: envelope parsing, error mapping, sync/async request execution."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Union

import httpx

from ._version import __version__
from .exceptions import error_for

DEFAULT_BASE_URL = "https://app.camelmailer.com"

DateTimeLike = Union[str, datetime]


def _parse(response: httpx.Response) -> Any:
    """Unwrap the CamelMailer response envelope, raising a typed error on failure."""
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict) and payload.get("status") == "error":
        error = payload.get("error") or {}
        raise error_for(
            error.get("message") or "Unknown API error",
            code=error.get("code"),
            status_code=response.status_code,
        )

    if response.status_code >= 400:
        raise error_for(
            f"Unexpected HTTP {response.status_code} response from the CamelMailer API",
            status_code=response.status_code,
        )

    if isinstance(payload, dict):
        return payload.get("data")

    raise error_for(
        "The response was not a CamelMailer API envelope",
        status_code=response.status_code,
    )


def build_query(**kwargs: Any) -> dict[str, Any]:
    """Drop ``None`` values and serialize datetimes to ISO 8601 strings."""
    query: dict[str, Any] = {}
    for key, value in kwargs.items():
        if value is None:
            continue
        if isinstance(value, datetime):
            value = value.isoformat()
        query[key] = value
    return query


class _TransportBase:
    def __init__(self, api_key: str, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "X-Server-API-Key": api_key,
            "User-Agent": f"camelmailer-python/{__version__}",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"


class SyncTransport(_TransportBase):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout)
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> Any:
        response = self._client.request(
            method,
            self._url(path),
            params=params,
            json=json,
            headers=self.headers,
        )
        return _parse(response)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


class AsyncTransport(_TransportBase):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout)
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> Any:
        response = await self._client.request(
            method,
            self._url(path),
            params=params,
            json=json,
            headers=self.headers,
        )
        return _parse(response)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
