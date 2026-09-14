"""Inbound and held messages (``/api/v2/server/inbound``).

Covers mail arriving through an inbound route as well as outbound mail the
spam filter put on hold, which is why a message here can be either retried
or released past the hold.
"""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport, build_query

_BASE = "/api/v2/server/inbound"


class Inbound:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        tag: str | None = None,
        query: str | None = None,
        stream: str | None = None,
    ) -> dict[str, Any]:
        """Search inbound and held messages, newest first."""
        return cast(
            dict[str, Any],
            self._transport.request(
                "GET",
                _BASE,
                params=build_query(
                    page=page, per_page=per_page, status=status, tag=tag, query=query, stream=stream
                ),
            ),
        )

    def get(self, message_id: int) -> dict[str, Any]:
        """Show one inbound message."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{message_id}"))

    def retry(self, message_id: int) -> dict[str, Any]:
        """Put a message back on the delivery queue."""
        return cast(dict[str, Any], self._transport.request("POST", f"{_BASE}/{message_id}/retry"))

    def bypass(self, message_id: int) -> dict[str, Any]:
        """Release a held message past the hold and deliver it."""
        return cast(dict[str, Any], self._transport.request("POST", f"{_BASE}/{message_id}/bypass"))


class AsyncInbound:
    """Async counterpart of :class:`Inbound`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        tag: str | None = None,
        query: str | None = None,
        stream: str | None = None,
    ) -> dict[str, Any]:
        """Search inbound and held messages, newest first."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "GET",
                _BASE,
                params=build_query(
                    page=page, per_page=per_page, status=status, tag=tag, query=query, stream=stream
                ),
            ),
        )

    async def get(self, message_id: int) -> dict[str, Any]:
        """Show one inbound message."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{message_id}"))

    async def retry(self, message_id: int) -> dict[str, Any]:
        """Put a message back on the delivery queue."""
        return cast(
            dict[str, Any], await self._transport.request("POST", f"{_BASE}/{message_id}/retry")
        )

    async def bypass(self, message_id: int) -> dict[str, Any]:
        """Release a held message past the hold and deliver it."""
        return cast(
            dict[str, Any], await self._transport.request("POST", f"{_BASE}/{message_id}/bypass")
        )
