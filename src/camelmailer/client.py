"""The CamelMailer client classes (sync and async)."""

from __future__ import annotations

import os
from types import TracebackType
from typing import Any, cast

import httpx

from ._transport import DEFAULT_BASE_URL, AsyncTransport, SyncTransport
from .resources import (
    AsyncBounces,
    AsyncCampaigns,
    AsyncDmarc,
    AsyncEmails,
    AsyncInbound,
    AsyncLayouts,
    AsyncLogs,
    AsyncStats,
    AsyncStreams,
    AsyncSubscribers,
    AsyncTemplates,
    Bounces,
    Campaigns,
    Dmarc,
    Emails,
    Inbound,
    Layouts,
    Logs,
    Stats,
    Streams,
    Subscribers,
    Templates,
)

API_KEY_ENV = "CAMELMAILER_API_KEY"
BASE_URL_ENV = "CAMELMAILER_BASE_URL"


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get(API_KEY_ENV)
    if not key:
        raise ValueError(
            f"No API key provided. Pass api_key=... or set the {API_KEY_ENV} environment variable."
        )
    return key


def _resolve_base_url(base_url: str | None) -> str:
    return (base_url or os.environ.get(BASE_URL_ENV) or DEFAULT_BASE_URL).rstrip("/")


class CamelMailer:
    """Synchronous client for the CamelMailer messaging API.

    Args:
        api_key: A server API key (falls back to ``CAMELMAILER_API_KEY``).
        base_url: Your instance URL for self-hosted installs
            (falls back to ``CAMELMAILER_BASE_URL``, then the cloud default).
        timeout: Request timeout in seconds.
        http_client: Optionally bring your own ``httpx.Client``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._transport = SyncTransport(
            _resolve_api_key(api_key), _resolve_base_url(base_url), timeout, http_client
        )
        self.emails = Emails(self._transport)
        self.templates = Templates(self._transport)
        self.streams = Streams(self._transport)
        self.stats = Stats(self._transport)
        self.bounces = Bounces(self._transport)
        self.campaigns = Campaigns(self._transport)
        self.subscribers = Subscribers(self._transport)
        self.layouts = Layouts(self._transport)
        self.inbound = Inbound(self._transport)
        self.logs = Logs(self._transport)
        self.dmarc = Dmarc(self._transport)

    @property
    def base_url(self) -> str:
        return self._transport.base_url

    def ping(self) -> dict[str, Any]:
        """Validate the server API key."""
        return cast(dict[str, Any], self._transport.request("GET", "/api/v2/server/ping"))

    def server(self) -> dict[str, Any]:
        """Show the authenticated server."""
        return cast(dict[str, Any], self._transport.request("GET", "/api/v2/server/"))

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> CamelMailer:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


class AsyncCamelMailer:
    """Asynchronous client for the CamelMailer messaging API.

    Accepts the same arguments as :class:`CamelMailer`; optionally bring
    your own ``httpx.AsyncClient``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._transport = AsyncTransport(
            _resolve_api_key(api_key), _resolve_base_url(base_url), timeout, http_client
        )
        self.emails = AsyncEmails(self._transport)
        self.templates = AsyncTemplates(self._transport)
        self.streams = AsyncStreams(self._transport)
        self.stats = AsyncStats(self._transport)
        self.bounces = AsyncBounces(self._transport)
        self.campaigns = AsyncCampaigns(self._transport)
        self.subscribers = AsyncSubscribers(self._transport)
        self.layouts = AsyncLayouts(self._transport)
        self.inbound = AsyncInbound(self._transport)
        self.logs = AsyncLogs(self._transport)
        self.dmarc = AsyncDmarc(self._transport)

    @property
    def base_url(self) -> str:
        return self._transport.base_url

    async def ping(self) -> dict[str, Any]:
        """Validate the server API key."""
        return cast(dict[str, Any], await self._transport.request("GET", "/api/v2/server/ping"))

    async def server(self) -> dict[str, Any]:
        """Show the authenticated server."""
        return cast(dict[str, Any], await self._transport.request("GET", "/api/v2/server/"))

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncCamelMailer:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()
