"""The server's own request log and tag index.

Useful when a send did not arrive and the question is whether the request
ever reached the API, and with what answer.
"""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, DateTimeLike, SyncTransport, build_query

_LOGS = "/api/v2/server/logs"
_TAGS = "/api/v2/server/tags"


class Logs:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        method: str | None = None,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
    ) -> dict[str, Any]:
        """List logged API requests, newest first.

        ``status`` is a class such as ``"4xx"``. ``from_`` carries the
        trailing underscore because ``from`` is a keyword; it is sent as
        ``from``.
        """
        return cast(
            dict[str, Any],
            self._transport.request(
                "GET",
                _LOGS,
                params=build_query(
                    page=page,
                    per_page=per_page,
                    status=status,
                    method=method,
                    **{"from": from_},
                    to=to,
                ),
            ),
        )

    def tags(self) -> dict[str, Any]:
        """Tags used by the server's recent messages, most used first."""
        return cast(dict[str, Any], self._transport.request("GET", _TAGS))


class AsyncLogs:
    """Async counterpart of :class:`Logs`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        method: str | None = None,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
    ) -> dict[str, Any]:
        """List logged API requests. See :meth:`Logs.list`."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "GET",
                _LOGS,
                params=build_query(
                    page=page,
                    per_page=per_page,
                    status=status,
                    method=method,
                    **{"from": from_},
                    to=to,
                ),
            ),
        )

    async def tags(self) -> dict[str, Any]:
        """Tags used by the server's recent messages, most used first."""
        return cast(dict[str, Any], await self._transport.request("GET", _TAGS))
