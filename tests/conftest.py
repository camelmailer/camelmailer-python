from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

import pytest

import camelmailer

API_KEY = "cm_test_key"
BASE_URL = "https://mailer.test"


@pytest.fixture
def client() -> Iterator[camelmailer.CamelMailer]:
    c = camelmailer.CamelMailer(api_key=API_KEY, base_url=BASE_URL)
    yield c
    c.close()


@pytest.fixture
async def aclient() -> AsyncIterator[camelmailer.AsyncCamelMailer]:
    c = camelmailer.AsyncCamelMailer(api_key=API_KEY, base_url=BASE_URL)
    yield c
    await c.aclose()
