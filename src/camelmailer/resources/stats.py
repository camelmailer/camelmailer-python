"""Message and delivery statistics (``/api/v2/server/stats``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, DateTimeLike, SyncTransport, build_query
from ..types import Stats as StatsData

_BASE = "/api/v2/server/stats"


class Stats:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def get(
        self,
        *,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
    ) -> StatsData:
        """Message counters, optionally limited to a time window."""
        data = self._transport.request(
            "GET", _BASE, params=build_query(**{"from": from_, "to": to})
        )
        if isinstance(data, dict) and isinstance(data.get("stats"), dict):
            return cast(StatsData, data["stats"])
        return cast(StatsData, data)

    def deliveries(self) -> dict[str, Any]:
        """Delivery/queue statistics."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/deliveries"))


class AsyncStats:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def get(
        self,
        *,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
    ) -> StatsData:
        """Message counters, optionally limited to a time window."""
        data = await self._transport.request(
            "GET", _BASE, params=build_query(**{"from": from_, "to": to})
        )
        if isinstance(data, dict) and isinstance(data.get("stats"), dict):
            return cast(StatsData, data["stats"])
        return cast(StatsData, data)

    async def deliveries(self) -> dict[str, Any]:
        """Delivery/queue statistics."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/deliveries"))
