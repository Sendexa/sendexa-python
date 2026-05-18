from .sms import SMSResource
from .otp import OTPResource
from .whatsapp import WhatsAppResource
from .email import EmailResource
from .voice import VoiceResource
from .webhooks import WebhooksResource

__all__ = [
    "SMSResource",
    "OTPResource",
    "WhatsAppResource",
    "EmailResource",
    "VoiceResource",
    "WebhooksResource",
]
