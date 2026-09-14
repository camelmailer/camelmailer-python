"""Template layouts (``/api/v2/server/layouts``).

A layout wraps every template that uses it, so header, footer and styling
live in one place instead of in each template.
"""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport
from ..types import LayoutCreateParams, LayoutUpdateParams

_BASE = "/api/v2/server/layouts"


class Layouts:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self) -> dict[str, Any]:
        """List all layouts of the server."""
        return cast(dict[str, Any], self._transport.request("GET", _BASE))

    def create(self, params: LayoutCreateParams) -> dict[str, Any]:
        """Create a layout.

        ``html_wrapper`` has to embed the body raw, as ``{{{ content }}}``.
        Escaped interpolation would show the message markup as text, so the
        API refuses it with ``ValidationError``.
        """
        return cast(dict[str, Any], self._transport.request("POST", _BASE, json=params))

    def get(self, permalink: str) -> dict[str, Any]:
        """Show a layout."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{permalink}"))

    def update(self, permalink: str, params: LayoutUpdateParams) -> dict[str, Any]:
        """Update a layout; only the given fields change."""
        return cast(
            dict[str, Any], self._transport.request("PATCH", f"{_BASE}/{permalink}", json=params)
        )

    def delete(self, permalink: str) -> dict[str, Any]:
        """Delete a layout. Templates that used it fall back to no wrapper."""
        return cast(dict[str, Any], self._transport.request("DELETE", f"{_BASE}/{permalink}"))

    def upload_logo(self, permalink: str, data_url: str) -> dict[str, Any]:
        """Upload the layout's logo as a ``data:image/png;base64,...`` URL.

        Returns the absolute URL to reference from the wrapper; it is served
        without authentication, because mail clients fetch it without a
        session.
        """
        return cast(
            dict[str, Any],
            self._transport.request(
                "POST", f"{_BASE}/{permalink}/logo", json={"data_url": data_url}
            ),
        )


class AsyncLayouts:
    """Async counterpart of :class:`Layouts`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self) -> dict[str, Any]:
        """List all layouts of the server."""
        return cast(dict[str, Any], await self._transport.request("GET", _BASE))

    async def create(self, params: LayoutCreateParams) -> dict[str, Any]:
        """Create a layout. See :meth:`Layouts.create`."""
        return cast(dict[str, Any], await self._transport.request("POST", _BASE, json=params))

    async def get(self, permalink: str) -> dict[str, Any]:
        """Show a layout."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{permalink}"))

    async def update(self, permalink: str, params: LayoutUpdateParams) -> dict[str, Any]:
        """Update a layout; only the given fields change."""
        return cast(
            dict[str, Any],
            await self._transport.request("PATCH", f"{_BASE}/{permalink}", json=params),
        )

    async def delete(self, permalink: str) -> dict[str, Any]:
        """Delete a layout."""
        return cast(dict[str, Any], await self._transport.request("DELETE", f"{_BASE}/{permalink}"))

    async def upload_logo(self, permalink: str, data_url: str) -> dict[str, Any]:
        """Upload the layout's logo. See :meth:`Layouts.upload_logo`."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "POST", f"{_BASE}/{permalink}/logo", json={"data_url": data_url}
            ),
        )
