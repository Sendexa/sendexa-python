from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Dict

from ..errors import SendexaError


class WebhooksResource:
    """Helpers for verifying and parsing Sendexa webhook events.

    These methods are pure functions — they do not need the HTTP client
    and work in any Python 3.9+ environment (standard library only).
    """

    def verify(self, signature: str, raw_body: str | bytes, secret: str) -> bool:
        """Verify the ``X-Sendexa-Signature`` header on an incoming webhook.

        Sendexa signs every webhook payload with HMAC-SHA256 using your
        webhook secret. Always verify before processing events.

        :param signature: Value of the ``X-Sendexa-Signature`` header (hex string).
        :param raw_body: The raw request body as ``str`` or ``bytes``.
        :param secret: Your webhook signing secret from the dashboard.
        :returns: ``True`` if the signature is valid.

        Example — Flask::

            @app.route('/webhook', methods=['POST'])
            def webhook():
                sig = request.headers.get('X-Sendexa-Signature', '')
                valid = client.webhooks.verify(sig, request.get_data(), secret)
                if not valid:
                    abort(401)
                event = client.webhooks.parse(request.get_data(as_text=True))
                return '', 200
        """
        if not signature or not secret:
            return False

        body_bytes = raw_body.encode() if isinstance(raw_body, str) else raw_body
        secret_bytes = secret.encode()

        # Strip the optional "sha256=" prefix
        sig_hex = signature.removeprefix("sha256=")

        expected = hmac.new(secret_bytes, body_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, sig_hex)

    def parse(self, raw_body: str) -> Dict[str, Any]:
        """Parse a raw webhook body into a dict.

        Does NOT verify the signature — call :meth:`verify` first.

        :raises SendexaError: if the payload is not valid JSON or is missing
            the ``event`` field.
        """
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise SendexaError(
                "Webhook payload is not valid JSON",
                400,
                "INVALID_WEBHOOK_PAYLOAD",
            ) from exc

        if not isinstance(payload, dict) or "event" not in payload:
            raise SendexaError(
                'Webhook payload is missing the "event" field',
                400,
                "INVALID_WEBHOOK_PAYLOAD",
            )

        return payload  # type: ignore[return-value]

    def is_event(self, event: Dict[str, Any], event_type: str) -> bool:
        """Return ``True`` if the parsed event matches *event_type*."""
        return event.get("event") == event_type
