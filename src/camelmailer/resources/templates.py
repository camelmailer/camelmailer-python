"""Manage stored templates (``/api/v2/server/templates``)."""

from __future__ import annotations

from typing import Any, cast

from .._transport import AsyncTransport, SyncTransport
from ..types import TemplateCreateParams, TemplateUpdateParams

_BASE = "/api/v2/server/templates"


class Templates:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self) -> dict[str, Any]:
        """List templates."""
        return cast(dict[str, Any], self._transport.request("GET", _BASE))

    def create(self, params: TemplateCreateParams) -> dict[str, Any]:
        """Create a template."""
        return cast(dict[str, Any], self._transport.request("POST", _BASE, json=params))

    def get(self, permalink: str) -> dict[str, Any]:
        """Show a template."""
        return cast(dict[str, Any], self._transport.request("GET", f"{_BASE}/{permalink}"))

    def update(self, permalink: str, params: TemplateUpdateParams) -> dict[str, Any]:
        """Update a template."""
        return cast(
            dict[str, Any],
            self._transport.request("PATCH", f"{_BASE}/{permalink}", json=params),
        )

    def archive(self, permalink: str) -> dict[str, Any]:
        """Archive a template."""
        return cast(dict[str, Any], self._transport.request("POST", f"{_BASE}/{permalink}/archive"))

    def render(
        self, permalink: str, template_model: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Render a template against a model (preview, does not send)."""
        return cast(
            dict[str, Any],
            self._transport.request(
                "POST",
                f"{_BASE}/{permalink}/render",
                json={"template_model": template_model or {}},
            ),
        )


class AsyncTemplates:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self) -> dict[str, Any]:
        """List templates."""
        return cast(dict[str, Any], await self._transport.request("GET", _BASE))

    async def create(self, params: TemplateCreateParams) -> dict[str, Any]:
        """Create a template."""
        return cast(dict[str, Any], await self._transport.request("POST", _BASE, json=params))

    async def get(self, permalink: str) -> dict[str, Any]:
        """Show a template."""
        return cast(dict[str, Any], await self._transport.request("GET", f"{_BASE}/{permalink}"))

    async def update(self, permalink: str, params: TemplateUpdateParams) -> dict[str, Any]:
        """Update a template."""
        return cast(
            dict[str, Any],
            await self._transport.request("PATCH", f"{_BASE}/{permalink}", json=params),
        )

    async def archive(self, permalink: str) -> dict[str, Any]:
        """Archive a template."""
        return cast(
            dict[str, Any],
            await self._transport.request("POST", f"{_BASE}/{permalink}/archive"),
        )

    async def render(
        self, permalink: str, template_model: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Render a template against a model (preview, does not send)."""
        return cast(
            dict[str, Any],
            await self._transport.request(
                "POST",
                f"{_BASE}/{permalink}/render",
                json={"template_model": template_model or {}},
            ),
        )
