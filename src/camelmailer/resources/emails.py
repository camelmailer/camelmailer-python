"""Send and inspect messages (``/api/v2/server/messages``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport, build_query
from ..types import MessageList, SendParams, SendResult, SendWithTemplateParams

_BASE = "/api/v2/server/messages"


class Emails:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def send(self, params: SendParams) -> SendResult:
        """Send a message; queues one message per recipient."""
        return cast(SendResult, self._transport.request("POST", _BASE, json=params))

    def send_batch(self, messages: list[SendParams]) -> dict[str, Any]:
        """Send a batch of messages; returns one result per entry."""
        return cast(
            dict[str, Any],
            self._transport.request("POST", f"{_BASE}/batch", json={"messages": messages}),
        )

    def send_with_template(self, params: SendWithTemplateParams) -> dict[str, Any]:
        """Render a stored template against ``template_model``, then send."""
        return cast(
            dict[str, Any],
            self._transport.request("POST", f"{_BASE}/with_template", json=params),
        )

    def send_with_template_batch(self, messages: list[SendWithTemplateParams]) -> dict[str, Any]:
        """Send a stored template to many recipients in one call."""
        return cast(
            dict[str, Any],
            self._transport.request(
                "POST", f"{_BASE}/with_template/batch", json={"messages": messages}
            ),
        )

    def get(self, message_id: int) -> dict[str, Any]:
        """Show a message."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{message_id}"))

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        scope: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        query: str | None = None,
        stream: str | None = None,
    ) -> MessageList:
        """List messages, filterable by scope/status/tag/query/stream."""
        return cast(
            MessageList,
            self._transport.request(
                "GET",
                _BASE,
                params=build_query(
                    page=page,
                    per_page=per_page,
                    scope=scope,
                    status=status,
                    tag=tag,
                    query=query,
                    stream=stream,
                ),
            ),
        )

    def deliveries(self, message_id: int) -> dict[str, Any]:
        """Delivery attempts of a message."""
        return cast(
            dict[str, Any],
            self._transport.request("GET", f"{_BASE}/{message_id}/deliveries"),
        )

    def opens(self, message_id: int) -> dict[str, Any]:
        """Open events of a message."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{message_id}/opens"))

    def clicks(self, message_id: int) -> dict[str, Any]:
        """Click events of a message."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{message_id}/clicks"))

    def raw(self, message_id: int) -> dict[str, Any]:
        """Raw RFC 5322 source of a message."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{message_id}/raw"))


class AsyncEmails:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def send(self, params: SendParams) -> SendResult:
        """Send a message; queues one message per recipient."""
        return cast(SendResult, await self._transport.request("POST", _BASE, json=params))

    async def send_batch(self, messages: list[SendParams]) -> dict[str, Any]:
        """Send a batch of messages; returns one result per entry."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_BASE}/batch", json={"messages": messages}),
        )

    async def send_with_template(self, params: SendWithTemplateParams) -> dict[str, Any]:
        """Render a stored template against ``template_model``, then send."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_BASE}/with_template", json=params),
        )

    async def send_with_template_batch(
        self, messages: list[SendWithTemplateParams]
    ) -> dict[str, Any]:
        """Send a stored template to many recipients in one call."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "POST", f"{_BASE}/with_template/batch", json={"messages": messages}
            ),
        )

    async def get(self, message_id: int) -> dict[str, Any]:
        """Show a message."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{message_id}"))

    async def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        scope: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        query: str | None = None,
        stream: str | None = None,
    ) -> MessageList:
        """List messages, filterable by scope/status/tag/query/stream."""
        return cast(
            MessageList,
            await self._transport.request(
                "GET",
                _BASE,
                params=build_query(
                    page=page,
                    per_page=per_page,
                    scope=scope,
                    status=status,
                    tag=tag,
                    query=query,
                    stream=stream,
                ),
            ),
        )

    async def deliveries(self, message_id: int) -> dict[str, Any]:
        """Delivery attempts of a message."""
        return cast(
            dict[str, Any],
            await self._transport.request("GET", f"{_BASE}/{message_id}/deliveries"),
        )

    async def opens(self, message_id: int) -> dict[str, Any]:
        """Open events of a message."""
        return cast(
            dict[str, Any],
            await self._transport.request("GET", f"{_BASE}/{message_id}/opens"),
        )

    async def clicks(self, message_id: int) -> dict[str, Any]:
        """Click events of a message."""
        return cast(
            dict[str, Any],
            await self._transport.request("GET", f"{_BASE}/{message_id}/clicks"),
        )

    async def raw(self, message_id: int) -> dict[str, Any]:
        """Raw RFC 5322 source of a message."""
        return cast(
            dict[str, Any],
            await self._transport.request("GET", f"{_BASE}/{message_id}/raw"),
        )
