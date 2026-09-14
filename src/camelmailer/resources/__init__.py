"""Resource namespaces of the CamelMailer messaging API."""

from .bounces import AsyncBounces, Bounces
from .campaigns import AsyncCampaigns, Campaigns
from .dmarc import AsyncDmarc, Dmarc
from .emails import AsyncEmails, Emails
from .inbound import AsyncInbound, Inbound
from .layouts import AsyncLayouts, Layouts
from .logs import AsyncLogs, Logs
from .stats import AsyncStats, Stats
from .streams import AsyncStreams, Streams
from .subscribers import AsyncSubscribers, Subscribers
from .templates import AsyncTemplates, Templates

__all__ = [
    "AsyncBounces",
    "AsyncCampaigns",
    "AsyncDmarc",
    "AsyncEmails",
    "AsyncInbound",
    "AsyncLayouts",
    "AsyncLogs",
    "AsyncStats",
    "AsyncStreams",
    "AsyncSubscribers",
    "AsyncTemplates",
    "Bounces",
    "Campaigns",
    "Dmarc",
    "Emails",
    "Inbound",
    "Layouts",
    "Logs",
    "Stats",
    "Streams",
    "Subscribers",
    "Templates",
]
