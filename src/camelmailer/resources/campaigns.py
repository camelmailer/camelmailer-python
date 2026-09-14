"""Broadcast campaigns (``/api/v2/server/campaigns``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport
from ..types import CampaignCreateParams, CampaignDraftParams, CampaignUpdateParams

_BASE = "/api/v2/server/campaigns"
_STREAMS = "/api/v2/server/streams"


class Campaigns:
    """A campaign is content plus an audience.

    There are two ways to create one and they behave differently:
    :meth:`create_draft` writes it and waits, while :meth:`create_and_send`
    expands it to the stream's subscribers before the call returns.
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

    def create_draft(self, params: CampaignDraftParams) -> dict[str, Any]:
        """Create a campaign without sending it.

        Name the audience with ``stream``. Leave ``scheduled_at`` out for a
        ``draft``, set it for ``scheduled``, or pass ``send_now`` to send on
        creation.
        """
        return cast(dict[str, Any], self._transport.request("POST", _BASE, json=params))

    def create_and_send(self, permalink: str, params: CampaignCreateParams) -> dict[str, Any]:
        """Create a campaign on a broadcast stream and send it immediately.

        The send starts before this call returns, so there is no draft to
        review and no schedule to set. Use :meth:`create_draft` when the
        campaign should wait.
        """
        return cast(
            dict[str, Any],
            self._transport.request("POST", f"{_STREAMS}/{permalink}/campaigns", json=params),
        )

    def create(self, permalink: str, params: CampaignCreateParams) -> dict[str, Any]:
        """Deprecated alias of :meth:`create_and_send`.

        Named ``create`` and documented as creating a draft in 0.2.0, which
        was wrong: it sends to the stream's subscribers straight away. For a
        draft, use :meth:`create_draft`.
        """
        return self.create_and_send(permalink, params)

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

    async def create_draft(self, params: CampaignDraftParams) -> dict[str, Any]:
        """Create a campaign without sending it. See :meth:`Campaigns.create_draft`."""
        return cast(dict[str, Any], await self._transport.request("POST", _BASE, json=params))

    async def create_and_send(self, permalink: str, params: CampaignCreateParams) -> dict[str, Any]:
        """Create and send immediately. See :meth:`Campaigns.create_and_send`."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_STREAMS}/{permalink}/campaigns", json=params),
        )

    async def create(self, permalink: str, params: CampaignCreateParams) -> dict[str, Any]:
        """Deprecated alias of :meth:`create_and_send`. See :meth:`Campaigns.create`."""
        return await self.create_and_send(permalink, params)

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
