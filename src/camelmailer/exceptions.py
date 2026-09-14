"""Typed errors raised by the CamelMailer SDK.

Every API error carries the stable error ``code`` from the response
envelope (``Unauthorized``, ``NotFound``, ``ValidationError``, …), the
human-readable ``message`` and the HTTP ``status_code``.
"""

from __future__ import annotations


class CamelMailerError(Exception):
    """Base class for all errors raised by this SDK."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(message={self.message!r}, "
            f"code={self.code!r}, status_code={self.status_code!r})"
        )


class AuthenticationError(CamelMailerError):
    """The API key is missing, invalid or not permitted (401/403)."""


class ValidationError(CamelMailerError):
    """The request was understood but invalid (422 / ValidationError / ParameterMissing)."""


class NotFoundError(CamelMailerError):
    """The requested resource does not exist (404)."""


class RateLimitError(CamelMailerError):
    """Too many requests (429), including a spent send allowance."""


class SendLimitExceededError(RateLimitError):
    """The server's 30-day send allowance is used up (429).

    Raised before anything is stored, so nothing was queued and the retry
    is yours to schedule.
    """


_CODE_TO_ERROR: dict[str, type[CamelMailerError]] = {
    "Unauthorized": AuthenticationError,
    "InvalidCredentials": AuthenticationError,
    "AccessDenied": AuthenticationError,
    "ValidationError": ValidationError,
    "ParameterMissing": ValidationError,
    "NotFound": NotFoundError,
    "RateLimited": RateLimitError,
    "RateLimitExceeded": RateLimitError,
    "SendLimitExceeded": SendLimitExceededError,
    # An Idempotency-Key reused for different content, or sent twice on one
    # request. The server answers 409.
    "InvalidIdempotentRequest": ValidationError,
}

_STATUS_TO_ERROR: dict[int, type[CamelMailerError]] = {
    400: ValidationError,
    401: AuthenticationError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitError,
}


def error_for(
    message: str,
    *,
    code: str | None = None,
    status_code: int | None = None,
) -> CamelMailerError:
    """Build the most specific error class for an API error response."""
    error_cls: type[CamelMailerError] = CamelMailerError
    if code is not None and code in _CODE_TO_ERROR:
        error_cls = _CODE_TO_ERROR[code]
    elif status_code is not None and status_code in _STATUS_TO_ERROR:
        error_cls = _STATUS_TO_ERROR[status_code]
    return error_cls(message, code=code, status_code=status_code)


__all__ = [
    "AuthenticationError",
    "CamelMailerError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]
