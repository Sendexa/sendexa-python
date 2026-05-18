from __future__ import annotations

from typing import Any

from .._client import HttpClient


class SMSResource:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def send(self, *, to: str, from_: str, message: str, **kwargs: Any) -> Any:
        """Send a single SMS message."""
        return self._client.post("/v1/sms/send", {"to": to, "from": from_, "message": message, **kwargs})

    def send_bulk(self, *, from_: str, messages: list[dict[str, Any]], message: str = "", **kwargs: Any) -> Any:
        """Send SMS to multiple recipients in one request."""
        return self._client.post("/v1/sms/bulk", {
            "from": from_,
            "message": message,
            "messages": messages,
            **kwargs,
        })

    def get_status(self, message_id: str) -> Any:
        """Retrieve the delivery status of a sent message."""
        return self._client.get(f"/v1/sms/status/{message_id}")

    def resend(self, message_id: str) -> Any:
        """Resend a previously failed or undelivered message."""
        return self._client.post(f"/v1/sms/resend/{message_id}")
