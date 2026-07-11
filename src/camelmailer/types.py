"""Typed request parameters and response shapes for the CamelMailer API."""

from __future__ import annotations

from typing import Any, Optional, TypedDict, Union


class _AddressObjectRequired(TypedDict):
    email: str


class AddressObject(_AddressObjectRequired, total=False):
    """An email address with an optional display name."""

    name: str


Address = Union[str, AddressObject]
"""Either a bare email string or an object with a display name."""


class Attachment(TypedDict):
    """A file attachment; ``data_base64`` is the base64-encoded content."""

    name: str
    content_type: str
    data_base64: str


SendParams = TypedDict(
    "SendParams",
    {
        "from": Address,
        "to": list[Address],
        "cc": list[Address],
        "bcc": list[Address],
        "reply_to": list[Address],
        "subject": str,
        "html_body": str,
        "text_body": str,
        "headers": dict[str, str],
        "attachments": list[Attachment],
        "tag": str,
        "metadata": dict[str, Any],
        "stream": str,
    },
    total=False,
)
"""Parameters for ``emails.send``; ``from`` and ``to`` are required by the API."""

SendWithTemplateParams = TypedDict(
    "SendWithTemplateParams",
    {
        "from": Address,
        "to": list[Address],
        "cc": list[Address],
        "bcc": list[Address],
        "reply_to": list[Address],
        "subject": str,
        "html_body": str,
        "text_body": str,
        "headers": dict[str, str],
        "attachments": list[Attachment],
        "tag": str,
        "metadata": dict[str, Any],
        "stream": str,
        "template": str,
        "template_model": dict[str, Any],
    },
    total=False,
)
"""Parameters for ``emails.send_with_template``; ``template`` names a stored template."""


class RecipientResult(TypedDict, total=False):
    rcpt_to: str
    status: str
    token: str


class SendResult(TypedDict, total=False):
    message_id: int
    recipients: list[RecipientResult]


class Pagination(TypedDict, total=False):
    page: int
    per_page: int
    total: int
    total_pages: int


class Message(TypedDict, total=False):
    id: int
    token: str
    scope: str
    rcpt_to: str
    mail_from: Optional[str]
    subject: Optional[str]
    message_id: Optional[str]
    tag: Optional[str]
    status: Optional[str]
    bounce: bool
    spam_status: Optional[str]
    spam_score: Optional[float]
    held: bool
    threat: bool
    size: Optional[int]
    metadata: Optional[dict[str, Any]]
    stream_id: Optional[int]
    bypassed: bool
    created_at: str


class MessageList(TypedDict, total=False):
    messages: list[Message]
    pagination: Pagination


class Stats(TypedDict, total=False):
    total: int
    incoming: int
    outgoing: int
    sent: int
    pending: int
    held: int
    bounced: int
    soft_fail: int
    hard_fail: int
    opens: int
    clicks: int
    unique_opens: int
    unique_clicks: int


class TemplateCreateParams(TypedDict, total=False):
    """``name`` is required; ``subject`` may contain ``{{ variables }}``."""

    name: str
    subject: str
    html_body: str
    text_body: str


class TemplateUpdateParams(TypedDict, total=False):
    name: str
    subject: str
    html_body: str
    text_body: str


class StreamCreateParams(TypedDict, total=False):
    """``name`` is required; ``stream_type`` is ``transactional`` or ``broadcast``."""

    name: str
    stream_type: str


class StreamUpdateParams(TypedDict, total=False):
    name: str
    stream_type: str


class DmarcSourceSummary(TypedDict, total=False):
    source_ip: str
    count: int
    spf_aligned_pct: float
    dkim_aligned_pct: float
    disposition_counts: dict[str, int]


DmarcSummary = TypedDict(
    "DmarcSummary",
    {
        "total": int,
        "pass": int,
        "fail": int,
        "pass_rate": float,
        "by_source": list[DmarcSourceSummary],
        "by_disposition": dict[str, int],
    },
    total=False,
)


class DmarcReport(TypedDict, total=False):
    id: int
    domain: str
    org_name: Optional[str]
    org_email: Optional[str]
    report_id: str
    date_range_begin: str
    date_range_end: str
    received_at: str
    record_count: int


class DmarcRecord(TypedDict, total=False):
    id: int
    source_ip: str
    count: int
    disposition: str
    dkim_result: Optional[str]
    spf_result: Optional[str]
    dkim_aligned: bool
    spf_aligned: bool
    header_from: Optional[str]
    envelope_from: Optional[str]


class DmarcReportList(TypedDict, total=False):
    reports: list[DmarcReport]
    pagination: Pagination


class DmarcReportDetail(TypedDict, total=False):
    report: DmarcReport
    records: list[DmarcRecord]


__all__ = [
    "Address",
    "AddressObject",
    "Attachment",
    "DmarcRecord",
    "DmarcReport",
    "DmarcReportDetail",
    "DmarcReportList",
    "DmarcSourceSummary",
    "DmarcSummary",
    "Message",
    "MessageList",
    "Pagination",
    "RecipientResult",
    "SendParams",
    "SendResult",
    "SendWithTemplateParams",
    "Stats",
    "StreamCreateParams",
    "StreamUpdateParams",
    "TemplateCreateParams",
    "TemplateUpdateParams",
]
