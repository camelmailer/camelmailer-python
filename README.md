# camelmailer-python

[![CI](https://github.com/camelmailer/camelmailer-python/actions/workflows/ci.yml/badge.svg)](https://github.com/camelmailer/camelmailer-python/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/camelmailer)](https://pypi.org/project/camelmailer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

The official Python SDK for [Camelmailer](https://camelmailer.com) — open-source transactional email.

Fully typed (`py.typed`), sync **and** async, one dependency (`httpx`), Python 3.9+.

## Install

```bash
pip install camelmailer
```

## Quickstart

```python
import camelmailer

client = camelmailer.CamelMailer(api_key="cm_xxxx")  # or set CAMELMAILER_API_KEY
result = client.emails.send({
    "from": "billing@yourdomain.com",
    "to": ["ada@example.com"],
    "subject": "Your receipt",
    "html_body": "<p>Thanks for your purchase!</p>",
})
print(result["message_id"])
```

The API key is a **server API key** (header `X-Server-API-Key`). If you don't pass
`api_key`, the client reads the `CAMELMAILER_API_KEY` environment variable.

## Self-hosted / custom instance

The default base URL is the Camelmailer cloud (`https://app.camelmailer.com`).
Point the client at your own instance:

```python
client = camelmailer.CamelMailer(api_key="cm_xxxx", base_url="https://mail.yourcompany.com")
```

…or set `CAMELMAILER_BASE_URL`.

## Async

```python
import asyncio, camelmailer

async def main() -> None:
    async with camelmailer.AsyncCamelMailer(api_key="cm_xxxx") as client:
        await client.emails.send({"from": "hi@yourdomain.com", "to": ["ada@example.com"],
                                  "subject": "Hello", "text_body": "Hi!"})

asyncio.run(main())
```

Every method below exists on both clients — identical signatures, just `await` them.

## Emails

```python
# Send (attachments, named addresses, tags, custom headers, metadata)
client.emails.send({
    "from": {"email": "billing@yourdomain.com", "name": "Acme Billing"},
    "to": ["ada@example.com"],
    "subject": "Invoice",
    "html_body": "<p>Attached.</p>",
    "attachments": [{"name": "invoice.pdf", "content_type": "application/pdf",
                     "data_base64": "aGVsbG8="}],
    "tag": "invoice",
})

# Batch
client.emails.send_batch([msg1, msg2, msg3])

# Stored templates (Mustache-style {{ variables }})
client.emails.send_with_template({
    "from": "hello@yourdomain.com",
    "to": ["ada@example.com"],
    "template": "welcome",
    "template_model": {"name": "Ada"},
})
client.emails.send_with_template_batch([...])

# Read back
client.emails.get(1234)
client.emails.list(scope="outgoing", status="Sent", tag="invoice", query="ada", page=1)
client.emails.deliveries(1234)
client.emails.opens(1234)
client.emails.clicks(1234)
client.emails.raw(1234)          # raw RFC 5322 source
```

## Templates

```python
client.templates.list()
client.templates.create({"name": "welcome", "subject": "Hi {{ name }}",
                         "html_body": "<p>Hi {{ name }}</p>"})
client.templates.get("welcome")
client.templates.update("welcome", {"subject": "Hello {{ name }}"})
client.templates.render("welcome", {"name": "Ada"})   # preview, does not send
client.templates.archive("welcome")
```

## Streams

```python
client.streams.list()
client.streams.create({"name": "Broadcasts", "stream_type": "broadcast"})
client.streams.get("broadcasts")
client.streams.update("broadcasts", {"name": "Newsletter"})
client.streams.archive("broadcasts")
```

## Stats & bounces

```python
client.stats.get(from_="2026-01-01T00:00:00Z")   # str or datetime
client.stats.deliveries()
client.bounces.list(page=1, per_page=25)
client.bounces.get(42)
```

## DMARC

```python
client.dmarc.summary(domain="yourdomain.com")
client.dmarc.reports(domain="yourdomain.com", page=1)
client.dmarc.report(7)   # single report incl. records
```

## Error handling

All API errors are typed exceptions carrying the stable error `code`, the
`message` and the HTTP `status_code`:

```python
import camelmailer

try:
    client.emails.send({"from": "no@unverified.example", "to": ["x@example.com"]})
except camelmailer.ValidationError as e:      # also: AuthenticationError,
    print(e.code, e.status_code, e.message)   # NotFoundError, RateLimitError
except camelmailer.CamelMailerError as e:     # base class for everything else
    print(e.code)
```

## Docs

Full API documentation: [camelmailer.com/docs](https://camelmailer.com/docs)

## License

[MIT](LICENSE)
