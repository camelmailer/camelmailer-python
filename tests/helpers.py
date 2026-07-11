from __future__ import annotations

import json
from typing import Any

import respx


def envelope(data: Any) -> dict[str, Any]:
    return {"status": "success", "time": 0.002, "data": data}


def error_envelope(code: str, message: str) -> dict[str, Any]:
    return {"status": "error", "time": 0.002, "error": {"code": code, "message": message}}


def last_request_json(route: respx.Route) -> Any:
    return json.loads(route.calls.last.request.content)
