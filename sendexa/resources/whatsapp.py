from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._client import HttpClient


class WhatsAppResource:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def send(self, body: Dict[str, Any]) -> Any:
        """Send a raw WhatsApp message payload."""
        return self._client.post("/v1/whatsapp/send", body)

    def send_text(self, to: str, text: str, *, preview_url: bool = False) -> Any:
        """Send a plain-text WhatsApp message."""
        return self.send({
            "to": to,
            "type": "text",
            "text": {"body": text, "preview_url": preview_url},
        })

    def send_image(self, to: str, url: str, caption: Optional[str] = None) -> Any:
        """Send an image message with an optional caption."""
        image: Dict[str, Any] = {"link": url}
        if caption:
            image["caption"] = caption
        return self.send({"to": to, "type": "image", "image": image})

    def send_document(
        self,
        to: str,
        url: str,
        *,
        caption: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Any:
        """Send a document / file attachment."""
        doc: Dict[str, Any] = {"link": url}
        if caption:
            doc["caption"] = caption
        if filename:
            doc["filename"] = filename
        return self.send({"to": to, "type": "document", "document": doc})

    def send_interactive(self, to: str, interactive: Dict[str, Any]) -> Any:
        """Send an interactive message (buttons, list, or CTA URL)."""
        return self.send({"to": to, "type": "interactive", "interactive": interactive})

    def send_template(self, to: str, template: Dict[str, Any]) -> Any:
        """Send an approved WhatsApp Business template message."""
        return self.send({"to": to, "type": "template", "template": template})

    def get_status(self, message_id: str) -> Any:
        """Get the delivery status of a WhatsApp message."""
        return self._client.get(f"/v1/whatsapp/status/{message_id}")

    def resend(self, message_id: str) -> Any:
        """Resend a failed WhatsApp message."""
        return self._client.post(f"/v1/whatsapp/resend/{message_id}")
