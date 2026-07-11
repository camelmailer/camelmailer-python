"""Integration tests against a real CamelMailer instance.

These are skipped unless ``CAMELMAILER_API_KEY`` is set (and optionally
``CAMELMAILER_BASE_URL`` for self-hosted instances). They are read-only:
they validate the key, list templates and read stats — no mail is sent.

Not part of CI.
"""

from __future__ import annotations

import os

import pytest

import camelmailer

pytestmark = pytest.mark.skipif(
    not os.environ.get("CAMELMAILER_API_KEY"),
    reason="CAMELMAILER_API_KEY is not set",
)


@pytest.fixture
def live_client() -> camelmailer.CamelMailer:
    return camelmailer.CamelMailer()


def test_roundtrip(live_client: camelmailer.CamelMailer) -> None:
    with live_client as client:
        client.ping()

        server = client.server()
        assert isinstance(server, dict)

        templates = client.templates.list()
        assert isinstance(templates, dict)

        stats = client.stats.get()
        assert isinstance(stats, dict)

        messages = client.emails.list(per_page=1)
        assert "messages" in messages


async def test_roundtrip_async() -> None:
    async with camelmailer.AsyncCamelMailer() as client:
        await client.ping()
        stats = await client.stats.get()
        assert isinstance(stats, dict)
