"""Manage message streams (``/api/v2/server/streams``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport
from ..types import StreamCreateParams, StreamUpdateParams

_BASE = "/api/v2/server/streams"


class Streams:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self) -> dict[str, Any]:
        """List message streams."""
        return cast(dict[str, Any], self._transport.request("GET", _BASE))

    def create(self, params: StreamCreateParams) -> dict[str, Any]:
        """Create a message stream."""
        return cast(dict[str, Any], self._transport.request("POST", _BASE, json=params))

    def get(self, permalink: str) -> dict[str, Any]:
        """Show a stream."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{permalink}"))

    def update(self, permalink: str, params: StreamUpdateParams) -> dict[str, Any]:
        """Update a stream."""
        return cast(
            dict[str, Any],
            self._transport.request("PATCH", f"{_BASE}/{permalink}", json=params),
        )

    def archive(self, permalink: str) -> dict[str, Any]:
        """Archive a stream."""
        return cast(dict[str, Any], self._transport.request("POST", f"{_BASE}/{permalink}/archive"))


class AsyncStreams:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self) -> dict[str, Any]:
        """List message streams."""
        return cast(dict[str, Any], await self._transport.request("GET", _BASE))

    async def create(self, params: StreamCreateParams) -> dict[str, Any]:
        """Create a message stream."""
        return cast(dict[str, Any], await self._transport.request("POST", _BASE, json=params))

    async def get(self, permalink: str) -> dict[str, Any]:
        """Show a stream."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{permalink}"))

    async def update(self, permalink: str, params: StreamUpdateParams) -> dict[str, Any]:
        """Update a stream."""
        return cast(
            dict[str, Any],
            await self._transport.request("PATCH", f"{_BASE}/{permalink}", json=params),
        )

    async def archive(self, permalink: str) -> dict[str, Any]:
        """Archive a stream."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_BASE}/{permalink}/archive"),
        )
