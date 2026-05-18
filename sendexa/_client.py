from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from typing import Any, Optional

from .errors import SendexaError

_DEFAULT_BASE_URL = "https://api.sendexa.co"
_DEFAULT_TIMEOUT = 30.0
_USER_AGENT = "sendexa-python/0.1.0"


def _snake_to_camel_from(key: str) -> str:
    """Map Python 'from_' param to JSON 'from' field."""
    return "from" if key == "from_" else key


def _prepare_body(body: Any) -> Any:
    """Recursively rename 'from_' keys to 'from' for JSON serialisation."""
    if isinstance(body, dict):
        return {_snake_to_camel_from(k): _prepare_body(v) for k, v in body.items()}
    if isinstance(body, list):
        return [_prepare_body(item) for item in body]
    return body


class HttpClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        token: Optional[str] = None,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        if token:
            self._auth = f"Basic {token}"
        elif api_key and api_secret:
            raw = f"{api_key}:{api_secret}".encode()
            self._auth = f"Basic {base64.b64encode(raw).decode()}"
        else:
            raise ValueError(
                "Provide either 'token' or both 'api_key' and 'api_secret'."
            )

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    # ------------------------------------------------------------------
    # Core request
    # ------------------------------------------------------------------

    def request(self, method: str, path: str, body: Any = None) -> Any:
        url = f"{self._base_url}{path}"
        payload = _prepare_body(body)
        data = json.dumps(payload).encode() if payload is not None else None

        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": self._auth,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": _USER_AGENT,
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            raw_body = exc.read().decode()
            try:
                err = json.loads(raw_body)
            except json.JSONDecodeError:
                err = {"message": raw_body}

            message: str = err.get("message", f"HTTP {exc.code}")
            code: str = err.get("code", "UNKNOWN_ERROR")
            request_id: Optional[str] = err.get("requestId") or err.get("request_id")
            raise SendexaError(message, exc.code, code, request_id, err) from exc
        except TimeoutError as exc:
            raise SendexaError("Request timed out", 408, "REQUEST_TIMEOUT") from exc

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, body: Any = None) -> Any:
        return self.request("POST", path, body)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)
