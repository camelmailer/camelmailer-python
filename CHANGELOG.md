# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
