"""Broadcast campaigns (``/api/v2/server/campaigns``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport
from ..types import CampaignCreateParams, CampaignUpdateParams

_BASE = "/api/v2/server/campaigns"
_STREAMS = "/api/v2/server/streams"


class Campaigns:
    """A campaign is content plus an audience.

    Creating one leaves it a ``draft``; scheduling and sending are separate
    calls, so nothing goes out as a side effect of writing it.
    """

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self) -> dict[str, Any]:
        """List every campaign on the server, newest first."""
        return cast(dict[str, Any], self._transport.request("GET", _BASE))

    def list_for_stream(self, permalink: str) -> dict[str, Any]:
        """List the campaigns of one broadcast stream."""
        return cast(
            dict[str, Any], self._transport.request("GET", f"{_STREAMS}/{permalink}/campaigns")
        )

    def get(self, campaign_id: int) -> dict[str, Any]:
        """Show a campaign together with its statistics."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{campaign_id}"))

    def get_for_stream(self, permalink: str, campaign_id: int) -> dict[str, Any]:
        """Show a campaign through its stream."""
        return cast(
            dict[str, Any],
            self._transport.request("GET", f"{_STREAMS}/{permalink}/campaigns/{campaign_id}"),
        )

    def create(self, permalink: str, params: CampaignCreateParams) -> dict[str, Any]:
        """Create a campaign on a broadcast stream. It starts as a draft."""
        return cast(
            dict[str, Any],
            self._transport.request("POST", f"{_STREAMS}/{permalink}/campaigns", json=params),
        )

    def update(self, campaign_id: int, params: CampaignUpdateParams) -> dict[str, Any]:
        """Update a draft or scheduled campaign.

        ``scheduled_at`` is three-valued: leave it out to keep the current
        schedule, give a timestamp to move a draft to ``scheduled``, or pass
        ``None`` to clear it and drop back to ``draft``.
        """
        return cast(
            dict[str, Any],
            self._transport.request("PATCH", f"{_BASE}/{campaign_id}", json=params),
        )

    def send(self, campaign_id: int) -> dict[str, Any]:
        """Send a campaign now, whatever its schedule said."""
        return cast(dict[str, Any], self._transport.request("POST", f"{_BASE}/{campaign_id}/send"))

    def cancel(self, campaign_id: int) -> dict[str, Any]:
        """Cancel a scheduled or in-flight campaign.

        Messages already queued are not recalled.
        """
        return cast(
            dict[str, Any], self._transport.request("POST", f"{_BASE}/{campaign_id}/cancel")
        )


class AsyncCampaigns:
    """Async counterpart of :class:`Campaigns`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self) -> dict[str, Any]:
        """List every campaign on the server, newest first."""
        return cast(dict[str, Any], await self._transport.request("GET", _BASE))

    async def list_for_stream(self, permalink: str) -> dict[str, Any]:
        """List the campaigns of one broadcast stream."""
        return cast(
            dict[str, Any],
            await self._transport.request("GET", f"{_STREAMS}/{permalink}/campaigns"),
        )

    async def get(self, campaign_id: int) -> dict[str, Any]:
        """Show a campaign together with its statistics."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{campaign_id}"))

    async def get_for_stream(self, permalink: str, campaign_id: int) -> dict[str, Any]:
        """Show a campaign through its stream."""
        return cast(
            dict[str, Any],
            await self._transport.request("GET", f"{_STREAMS}/{permalink}/campaigns/{campaign_id}"),
        )

    async def create(self, permalink: str, params: CampaignCreateParams) -> dict[str, Any]:
        """Create a campaign on a broadcast stream. It starts as a draft."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_STREAMS}/{permalink}/campaigns", json=params),
        )

    async def update(self, campaign_id: int, params: CampaignUpdateParams) -> dict[str, Any]:
        """Update a draft or scheduled campaign. See :meth:`Campaigns.update`."""
        return cast(
            dict[str, Any],
            await self._transport.request("PATCH", f"{_BASE}/{campaign_id}", json=params),
        )

    async def send(self, campaign_id: int) -> dict[str, Any]:
        """Send a campaign now, whatever its schedule said."""
        return cast(
            dict[str, Any], await self._transport.request("POST", f"{_BASE}/{campaign_id}/send")
        )

    async def cancel(self, campaign_id: int) -> dict[str, Any]:
        """Cancel a scheduled or in-flight campaign."""
        return cast(
            dict[str, Any], await self._transport.request("POST", f"{_BASE}/{campaign_id}/cancel")
        )
