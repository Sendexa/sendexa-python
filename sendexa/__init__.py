from __future__ import annotations

from typing import Optional

from ._client import HttpClient
from .errors import SendexaError
from .resources.sms import SMSResource
from .resources.otp import OTPResource
from .resources.whatsapp import WhatsAppResource
from .resources.email import EmailResource
from .resources.voice import VoiceResource
from .resources.webhooks import WebhooksResource

__version__ = "0.1.0"
__all__ = ["Sendexa", "SendexaError"]


class Sendexa:
    """The official Sendexa Python SDK client.

    Create one instance per application and reuse it — the client is
    stateless and safe to share across threads and requests.

    Authentication — provide one of:

    * ``api_key`` + ``api_secret`` — credentials from your dashboard.
    * ``token`` — a pre-computed Base64 token (``api_key:api_secret``).

    Example::

        from sendexa import Sendexa

        client = Sendexa(
            api_key="key_...",
            api_secret="secret_...",
        )

        # Send an SMS
        response = client.sms.send(
            to="0244123456",
            from_="MyBrand",
            message="Hello!",
        )
        print(response["data"]["messageId"])
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        token: Optional[str] = None,
        base_url: str = "https://api.sendexa.co",
        timeout: float = 30.0,
    ) -> None:
        http = HttpClient(
            api_key=api_key,
            api_secret=api_secret,
            token=token,
            base_url=base_url,
            timeout=timeout,
        )

        self.sms = SMSResource(http)
        self.otp = OTPResource(http)
        self.whatsapp = WhatsAppResource(http)
        self.email = EmailResource(http)
        self.voice = VoiceResource(http)
        self.webhooks = WebhooksResource()
