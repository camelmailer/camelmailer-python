# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-09-14

### Fixed

- **`send_batch` and `send_with_template_batch` never worked.** They wrapped
  the messages in `{"messages": [...]}` while the endpoint deserializes a
  bare array, so the API answered `invalid type: map, expected a sequence`.
  The tests asserted the wrapper, which is why it survived: they checked
  what the SDK sent rather than what the server accepts.

### Added

- **Broadcast campaigns** (`campaigns`), sync and async: list server-wide or
  per stream, create, update, send, cancel, and read per-campaign
  statistics. `scheduled_at` is three-valued: leave it out to keep the
  schedule, give a timestamp to move a draft to `scheduled`, pass `None` to
  clear it back to `draft`.
- **Subscribers** (`subscribers`): list, add, `import_`, remove and
  `complaint`. Addresses are percent-encoded, so a `+` in an address is no
  longer read as a space.
- **Layouts** (`layouts`): list, create, get, update, delete, `upload_logo`.
- **Inbound and held mail** (`inbound`): list with filters, get, retry,
  bypass.
- **Request log and tags** (`logs`): `list` with status-class and method
  filters, and `tags`.
- **`emails.send_to_stream`**: the same content to every subscriber of a
  broadcast stream, reporting `queued` against `skipped`.
- **Idempotent sending**: `send` and `send_batch` take
  `idempotency_key=...`, sent as the `Idempotency-Key` header. A retry
  replays the original result rather than queuing a second copy.
- `SendLimitExceededError`, a subclass of `RateLimitError`, so existing
  handlers keep working. `InvalidIdempotentRequest` maps to
  `ValidationError`.

### Note

These surfaces were missing because they were never in the OpenAPI spec
this SDK is written from, although the server has served them since v0.5.

## [0.1.0] - 2026-07-11

### Added

- Initial release.
- `CamelMailer` (sync) and `AsyncCamelMailer` (async) clients with
  configurable `base_url` for self-hosted instances and
  `CAMELMAILER_API_KEY` / `CAMELMAILER_BASE_URL` environment fallbacks.
- Resources: `emails` (send, send_batch, send_with_template,
  send_with_template_batch, get, list, deliveries, opens, clicks, raw),
  `templates` (list, create, get, update, archive, render),
  `streams` (list, create, get, update, archive),
  `stats` (get, deliveries), `bounces` (list, get),
  `dmarc` (summary, reports, report), plus `ping()` and `server()`.
- Typed exceptions with `.code` / `.message` / `.status_code`:
  `CamelMailerError`, `AuthenticationError`, `ValidationError`,
  `NotFoundError`, `RateLimitError`.
- Full type hints, TypedDict request/response shapes, `py.typed`.

[Unreleased]: https://github.com/camelmailer/camelmailer-python/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/camelmailer/camelmailer-python/releases/tag/v0.1.0
