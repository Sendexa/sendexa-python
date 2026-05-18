from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


# ---------------------------------------------------------------------------
# Generic
# ---------------------------------------------------------------------------

class ApiResponse(TypedDict):
    success: bool
    message: str
    data: Any


# ---------------------------------------------------------------------------
# SMS
# ---------------------------------------------------------------------------

class SendSMSRequest(TypedDict, total=False):
    to: str           # required
    from_: str        # required  (mapped to "from" on the wire)
    message: str      # required
    callbackUrl: str


class BulkSMSMessage(TypedDict, total=False):
    to: str           # required
    message: str      # overrides shared message


class SendBulkSMSRequest(TypedDict, total=False):
    from_: str        # required
    message: str      # shared fallback message
    messages: List[BulkSMSMessage]   # required
    callbackUrl: str


class SMSData(TypedDict):
    messageId: str
    status: str
    to: str
    from_: str
    createdAt: str


class BulkSMSData(TypedDict):
    batchId: str
    total: int
    queued: int
    failed: int


# ---------------------------------------------------------------------------
# OTP
# ---------------------------------------------------------------------------

OTPPinType = Literal["NUMERIC", "ALPHANUMERIC", "ALPHABETIC"]


class OTPExpiry(TypedDict, total=False):
    amount: int       # required
    duration: str     # required  e.g. "minutes"


class RequestOTPRequest(TypedDict, total=False):
    phone: str        # required
    from_: str        # required
    message: str
    pinLength: int
    pinType: OTPPinType
    expiry: OTPExpiry
    maxAmountOfValidationRetries: int
    metadata: Dict[str, Any]


class OTPData(TypedDict):
    id: str
    status: str
    phone: str
    expiry: OTPExpiry


class VerifyOTPRequest(TypedDict, total=False):
    id: str           # required
    pin: str          # required


class VerifyOTPData(TypedDict):
    id: str
    verified: bool
    attemptsRemaining: int


# ---------------------------------------------------------------------------
# WhatsApp
# ---------------------------------------------------------------------------

class WhatsAppTextMessage(TypedDict, total=False):
    type: Literal["text"]   # required
    to: str                  # required
    text: Dict[str, Any]     # {"body": "...", "preview_url": bool}


class WhatsAppMediaMessage(TypedDict, total=False):
    type: Literal["image", "video", "audio", "document"]  # required
    to: str                   # required
    image: Dict[str, Any]
    video: Dict[str, Any]
    audio: Dict[str, Any]
    document: Dict[str, Any]
    caption: str


class WhatsAppInteractive(TypedDict, total=False):
    type: str         # "button" | "list" | "cta_url"
    header: Dict[str, Any]
    body: Dict[str, Any]
    footer: Dict[str, Any]
    action: Dict[str, Any]


class WhatsAppTemplate(TypedDict, total=False):
    name: str         # required
    language: Dict[str, Any]   # {"code": "en"}
    components: List[Dict[str, Any]]


class SendWhatsAppRequest(TypedDict, total=False):
    to: str           # required
    type: str         # required
    text: Dict[str, Any]
    image: Dict[str, Any]
    video: Dict[str, Any]
    audio: Dict[str, Any]
    document: Dict[str, Any]
    interactive: WhatsAppInteractive
    template: WhatsAppTemplate


class WhatsAppData(TypedDict):
    messageId: str
    status: str
    to: str


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------

class EmailAttachment(TypedDict, total=False):
    filename: str     # required
    content: str      # required  base64-encoded
    contentType: str


class SendEmailRequest(TypedDict, total=False):
    to: str           # required
    from_: str        # required
    subject: str      # required
    html: str
    text: str
    replyTo: str
    attachments: List[EmailAttachment]
    metadata: Dict[str, Any]


class BulkEmailMessage(TypedDict, total=False):
    to: str           # required
    subject: str
    variables: Dict[str, Any]


class SendBulkEmailRequest(TypedDict, total=False):
    from_: str        # required
    subject: str      # required
    html: str
    text: str
    messages: List[BulkEmailMessage]   # required


class SendEmailWithTemplateRequest(TypedDict, total=False):
    to: str           # required
    from_: str        # required
    templateId: str   # required
    variables: Dict[str, Any]
    subject: str


class EmailData(TypedDict):
    messageId: str
    status: str
    to: str


# ---------------------------------------------------------------------------
# Voice
# ---------------------------------------------------------------------------

VoiceCallStatus = Literal[
    "queued", "ringing", "in-progress", "completed",
    "busy", "no-answer", "canceled", "failed",
]


class MakeCallRequest(TypedDict, total=False):
    to: str           # required
    from_: str        # required
    twiml: str
    url: str
    record: bool
    statusCallbackUrl: str
    machineDetection: bool


class TextToSpeechRequest(TypedDict, total=False):
    to: str           # required
    from_: str        # required
    text: str         # required
    language: str
    voice: str
    loop: int


class PlayAudioRequest(TypedDict, total=False):
    to: str           # required
    from_: str        # required
    audioUrl: str     # required
    loop: int


class CallData(TypedDict):
    callId: str
    status: VoiceCallStatus
    to: str
    from_: str
    duration: Optional[int]
    createdAt: str


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------

WebhookEventType = Literal[
    "message.sent",
    "message.delivered",
    "message.failed",
    "message.inbound",
    "otp.sent",
    "otp.verified",
    "otp.failed",
    "otp.expired",
    "call.initiated",
    "call.ringing",
    "call.answered",
    "call.completed",
    "call.failed",
    "email.delivered",
    "email.bounced",
    "email.opened",
]


class WebhookEvent(TypedDict, total=False):
    event: WebhookEventType   # required
    data: Any
    timestamp: str
    version: str
