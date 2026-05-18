from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from .._client import HttpClient

OTPPinType = Literal["NUMERIC", "ALPHANUMERIC", "ALPHABETIC"]


class OTPResource:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def request(
        self,
        *,
        phone: str,
        from_: str,
        message: str = "Your verification code is {code}. Valid for {amount} {duration}.",
        pin_length: int = 6,
        pin_type: OTPPinType = "NUMERIC",
        expiry: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Request a new OTP to be sent to the given phone number."""
        body: Dict[str, Any] = {
            "phone": phone,
            "from": from_,
            "message": message,
            "pinLength": pin_length,
            "pinType": pin_type,
            "maxAmountOfValidationRetries": max_retries,
        }
        if expiry is not None:
            body["expiry"] = expiry
        if metadata is not None:
            body["metadata"] = metadata
        body.update(kwargs)
        return self._client.post("/v1/otp/request", body)

    def verify(self, *, id: str, pin: str) -> Any:
        """Verify the PIN a user entered against the OTP session."""
        return self._client.post("/v1/otp/verify", {"id": id, "pin": pin})

    def resend(self, otp_id: str) -> Any:
        """Resend an OTP to the same phone number (subject to cooldown)."""
        return self._client.post(f"/v1/otp/resend/{otp_id}")
