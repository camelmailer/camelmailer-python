"""Opt-in subscribers of a broadcast stream.

Subscribers are wired to one stream rather than to a global contact list,
so the same address can be subscribed to one stream and not another. A
broadcast to an address that is not subscribed is refused, which makes this
list the audience rather than a convenience.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast
from urllib.parse import quote

from .._transport import AsyncTransport, SyncTransport
from ..types import SubscriberAddParams

_STREAMS = "/api/v2/server/streams"


def _base(permalink: str) -> str:
    return f"{_STREAMS}/{permalink}/subscribers"


def _address(permalink: str, address: str) -> str:
    # quote() with no safe characters, so a + in an address survives as %2B
    # rather than arriving as a space.
    return f"{_base(permalink)}/{quote(address, safe='')}"


class Subscribers:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self, permalink: str) -> dict[str, Any]:
        """List the stream's subscribers, subscribed and unsubscribed alike."""
        return cast(dict[str, Any], self._transport.request("GET", _base(permalink)))

    def add(self, permalink: str, params: SubscriberAddParams) -> dict[str, Any]:
        """Add or update one subscriber. Upserts by address."""
        return cast(dict[str, Any], self._transport.request("POST", _base(permalink), json=params))

    def import_(self, permalink: str, addresses: Sequence[str]) -> dict[str, Any]:
        """Add many addresses at once, all as ``subscribed``.

        Blanks and duplicates within the request are skipped; the response
        reports how many were written against how many survived that.

        Named with a trailing underscore because ``import`` is a keyword.
        """
        return cast(
            dict[str, Any],
            self._transport.request(
                "POST", f"{_base(permalink)}/import", json={"addresses": list(addresses)}
            ),
        )

    def remove(self, permalink: str, address: str) -> dict[str, Any]:
        """Remove a subscriber from the stream entirely."""
        return cast(dict[str, Any], self._transport.request("DELETE", _address(permalink, address)))

    def complaint(self, permalink: str, address: str) -> dict[str, Any]:
        """Record a spam complaint: a stream-scoped suppression plus an
        unsubscribe, in one idempotent call."""
        return cast(
            dict[str, Any],
            self._transport.request("POST", f"{_address(permalink, address)}/complaint"),
        )


class AsyncSubscribers:
    """Async counterpart of :class:`Subscribers`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self, permalink: str) -> dict[str, Any]:
        """List the stream's subscribers."""
        return cast(dict[str, Any], await self._transport.request("GET", _base(permalink)))

    async def add(self, permalink: str, params: SubscriberAddParams) -> dict[str, Any]:
        """Add or update one subscriber."""
        return cast(
            dict[str, Any], await self._transport.request("POST", _base(permalink), json=params)
        )

    async def import_(self, permalink: str, addresses: Sequence[str]) -> dict[str, Any]:
        """Add many addresses at once. See :meth:`Subscribers.import_`."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "POST", f"{_base(permalink)}/import", json={"addresses": list(addresses)}
            ),
        )

    async def remove(self, permalink: str, address: str) -> dict[str, Any]:
        """Remove a subscriber from the stream entirely."""
        return cast(
            dict[str, Any], await self._transport.request("DELETE", _address(permalink, address))
        )

    async def complaint(self, permalink: str, address: str) -> dict[str, Any]:
        """Record a spam complaint against an address."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_address(permalink, address)}/complaint"),
        )
