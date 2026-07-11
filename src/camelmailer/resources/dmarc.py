"""DMARC aggregate reports and compliance summary (``/api/v2/server/dmarc``)."""

from __future__ import annotations

from typing import cast

from .._transport import AsyncTransport, DateTimeLike, SyncTransport, build_query
from ..types import DmarcReportDetail, DmarcReportList, DmarcSummary

_BASE = "/api/v2/server/dmarc"


class Dmarc:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def summary(
        self,
        *,
        domain: str | None = None,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
    ) -> DmarcSummary:
        """DMARC compliance summary aggregated from stored reports."""
        data = self._transport.request(
            "GET",
            f"{_BASE}/summary",
            params=build_query(**{"domain": domain, "from": from_, "to": to}),
        )
        if isinstance(data, dict) and isinstance(data.get("summary"), dict):
            return cast(DmarcSummary, data["summary"])
        return cast(DmarcSummary, data)

    def reports(
        self,
        *,
        domain: str | None = None,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> DmarcReportList:
        """List stored DMARC aggregate reports, newest report range first."""
        return cast(
            DmarcReportList,
            self._transport.request(
                "GET",
                f"{_BASE}/reports",
                params=build_query(
                    **{"domain": domain, "from": from_, "to": to},
                    page=page,
                    per_page=per_page,
                ),
            ),
        )

    def report(self, report_id: int) -> DmarcReportDetail:
        """Show a DMARC report with its records."""
        return cast(
            DmarcReportDetail,
            self._transport.request("GET", f"{_BASE}/reports/{report_id}"),
        )


class AsyncDmarc:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def summary(
        self,
        *,
        domain: str | None = None,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
    ) -> DmarcSummary:
        """DMARC compliance summary aggregated from stored reports."""
        data = await self._transport.request(
            "GET",
            f"{_BASE}/summary",
            params=build_query(**{"domain": domain, "from": from_, "to": to}),
        )
        if isinstance(data, dict) and isinstance(data.get("summary"), dict):
            return cast(DmarcSummary, data["summary"])
        return cast(DmarcSummary, data)

    async def reports(
        self,
        *,
        domain: str | None = None,
        from_: DateTimeLike | None = None,
        to: DateTimeLike | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> DmarcReportList:
        """List stored DMARC aggregate reports, newest report range first."""
        return cast(
            DmarcReportList,
            await self._transport.request(
                "GET",
                f"{_BASE}/reports",
                params=build_query(
                    **{"domain": domain, "from": from_, "to": to},
                    page=page,
                    per_page=per_page,
                ),
            ),
        )

    async def report(self, report_id: int) -> DmarcReportDetail:
        """Show a DMARC report with its records."""
        return cast(
            DmarcReportDetail,
            await self._transport.request("GET", f"{_BASE}/reports/{report_id}"),
        )
