from __future__ import annotations

import httpx
import respx

import camelmailer
from conftest import BASE_URL
from helpers import envelope

DMARC = f"{BASE_URL}/api/v2/server/dmarc"

SUMMARY = {
    "total": 100,
    "pass": 95,
    "fail": 5,
    "pass_rate": 0.95,
    "by_source": [{"source_ip": "203.0.113.10", "count": 80}],
    "by_disposition": {"none": 100},
}

REPORT = {
    "id": 1,
    "domain": "acme.com",
    "org_name": "google.com",
    "report_id": "r-1",
    "record_count": 2,
}


@respx.mock
def test_summary(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{DMARC}/summary").mock(
        return_value=httpx.Response(200, json=envelope({"summary": SUMMARY}))
    )
    summary = client.dmarc.summary(domain="acme.com", from_="2026-01-01T00:00:00Z")
    assert summary["pass_rate"] == 0.95
    assert summary["by_source"][0]["source_ip"] == "203.0.113.10"
    params = dict(route.calls.last.request.url.params)
    assert params == {"domain": "acme.com", "from": "2026-01-01T00:00:00Z"}


@respx.mock
def test_reports(client: camelmailer.CamelMailer) -> None:
    route = respx.get(f"{DMARC}/reports").mock(
        return_value=httpx.Response(
            200,
            json=envelope(
                {"reports": [REPORT], "pagination": {"page": 1, "per_page": 25, "total": 1}}
            ),
        )
    )
    result = client.dmarc.reports(domain="acme.com", page=1, per_page=25)
    assert result["reports"][0]["domain"] == "acme.com"
    params = dict(route.calls.last.request.url.params)
    assert params == {"domain": "acme.com", "page": "1", "per_page": "25"}


@respx.mock
def test_report_detail(client: camelmailer.CamelMailer) -> None:
    respx.get(f"{DMARC}/reports/1").mock(
        return_value=httpx.Response(
            200,
            json=envelope(
                {"report": REPORT, "records": [{"source_ip": "203.0.113.10", "count": 2}]}
            ),
        )
    )
    detail = client.dmarc.report(1)
    assert detail["report"]["id"] == 1
    assert detail["records"][0]["count"] == 2


@respx.mock
async def test_async_summary(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{DMARC}/summary").mock(
        return_value=httpx.Response(200, json=envelope({"summary": SUMMARY}))
    )
    summary = await aclient.dmarc.summary()
    assert summary["total"] == 100


@respx.mock
async def test_async_reports(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{DMARC}/reports").mock(
        return_value=httpx.Response(200, json=envelope({"reports": [], "pagination": {}}))
    )
    result = await aclient.dmarc.reports()
    assert result["reports"] == []


@respx.mock
async def test_async_report_detail(aclient: camelmailer.AsyncCamelMailer) -> None:
    respx.get(f"{DMARC}/reports/7").mock(
        return_value=httpx.Response(200, json=envelope({"report": REPORT, "records": []}))
    )
    detail = await aclient.dmarc.report(7)
    assert detail["records"] == []
