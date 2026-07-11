"""Bounce messages (``/api/v2/server/bounces``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport, build_query

_BASE = "/api/v2/server/bounces"


class Bounces:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self, *, page: int | None = None, per_page: int | None = None) -> dict[str, Any]:
        """List bounce messages."""
        return cast(
            dict[str, Any],
            self._transport.request("GET", _BASE, params=build_query(page=page, per_page=per_page)),
        )

    def get(self, bounce_id: int) -> dict[str, Any]:
        """Show a bounce."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{bounce_id}"))


class AsyncBounces:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self, *, page: int | None = None, per_page: int | None = None) -> dict[str, Any]:
        """List bounce messages."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "GET", _BASE, params=build_query(page=page, per_page=per_page)
            ),
        )

    async def get(self, bounce_id: int) -> dict[str, Any]:
        """Show a bounce."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{bounce_id}"))
