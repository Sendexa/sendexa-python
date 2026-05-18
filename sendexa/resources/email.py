from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._client import HttpClient


class EmailResource:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def send(
        self,
        *,
        to: str,
        from_: str,
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Send a single transactional or marketing email."""
        body: Dict[str, Any] = {
            "to": to,
            "from": from_,
            "subject": subject,
        }
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if reply_to is not None:
            body["replyTo"] = reply_to
        if attachments is not None:
            body["attachments"] = attachments
        if metadata is not None:
            body["metadata"] = metadata
        body.update(kwargs)
        return self._client.post("/v1/email/send", body)

    def send_bulk(
        self,
        *,
        from_: str,
        subject: str,
        messages: List[Dict[str, Any]],
        html: Optional[str] = None,
        text: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Send the same email to multiple recipients."""
        body: Dict[str, Any] = {
            "from": from_,
            "subject": subject,
            "messages": messages,
        }
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        body.update(kwargs)
        return self._client.post("/v1/email/bulk", body)

    def send_with_template(
        self,
        *,
        to: str,
        from_: str,
        template_id: str,
        variables: Optional[Dict[str, Any]] = None,
        subject: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Send an email using a pre-built dashboard template."""
        body: Dict[str, Any] = {
            "to": to,
            "from": from_,
            "templateId": template_id,
        }
        if variables is not None:
            body["variables"] = variables
        if subject is not None:
            body["subject"] = subject
        body.update(kwargs)
        return self._client.post("/v1/email/send", body)

    def get_status(self, message_id: str) -> Any:
        """Get the delivery status of a sent email."""
        return self._client.get(f"/v1/email/status/{message_id}")
