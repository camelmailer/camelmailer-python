"""camelmailer — the official Python SDK for CamelMailer.

Usage::

    import camelmailer

    client = camelmailer.CamelMailer(api_key="cm_...")
    client.emails.send({"from": "you@yourdomain.com", "to": ["ada@example.com"],
                        "subject": "Hello", "text_body": "Hi!"})
"""

from . import exceptions, types
from ._transport import DEFAULT_BASE_URL
from ._version import __version__
from .client import API_KEY_ENV, BASE_URL_ENV, AsyncCamelMailer, CamelMailer
from .exceptions import (
    AuthenticationError,
    CamelMailerError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__all__ = [
    "API_KEY_ENV",
    "BASE_URL_ENV",
    "DEFAULT_BASE_URL",
    "AsyncCamelMailer",
    "AuthenticationError",
    "CamelMailer",
    "CamelMailerError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "__version__",
    "exceptions",
    "types",
]
