"""Resource namespaces of the CamelMailer messaging API."""

from .bounces import AsyncBounces, Bounces
from .dmarc import AsyncDmarc, Dmarc
from .emails import AsyncEmails, Emails
from .stats import AsyncStats, Stats
from .streams import AsyncStreams, Streams
from .templates import AsyncTemplates, Templates

__all__ = [
    "AsyncBounces",
    "AsyncDmarc",
    "AsyncEmails",
    "AsyncStats",
    "AsyncStreams",
    "AsyncTemplates",
    "Bounces",
    "Dmarc",
    "Emails",
    "Stats",
    "Streams",
    "Templates",
]
