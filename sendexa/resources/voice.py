from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from .._client import HttpClient


class VoiceResource:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def call(
        self,
        *,
        to: str,
        from_: str,
        twiml: Optional[str] = None,
        url: Optional[str] = None,
        record: bool = False,
        status_callback_url: Optional[str] = None,
        machine_detection: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Initiate a programmatic outbound call."""
        body: Dict[str, Any] = {"to": to, "from": from_, "record": record, "machineDetection": machine_detection}
        if twiml is not None:
            body["twiml"] = twiml
        if url is not None:
            body["url"] = url
        if status_callback_url is not None:
            body["statusCallbackUrl"] = status_callback_url
        body.update(kwargs)
        return self._client.post("/v1/voice/call", body)

    def tts(
        self,
        *,
        to: str,
        from_: str,
        text: str,
        language: str = "en-US",
        voice: Literal["male", "female"] = "female",
        loop: int = 1,
        **kwargs: Any,
    ) -> Any:
        """Make an outbound call that reads text aloud (text-to-speech)."""
        body: Dict[str, Any] = {
            "to": to,
            "from": from_,
            "text": text,
            "language": language,
            "voice": voice,
            "loop": loop,
        }
        body.update(kwargs)
        return self._client.post("/v1/voice/tts", body)

    def play(
        self,
        *,
        to: str,
        from_: str,
        audio_url: str,
        loop: int = 1,
        **kwargs: Any,
    ) -> Any:
        """Make an outbound call that plays an audio file."""
        body: Dict[str, Any] = {
            "to": to,
            "from": from_,
            "audioUrl": audio_url,
            "loop": loop,
        }
        body.update(kwargs)
        return self._client.post("/v1/voice/play", body)

    def get_status(self, call_id: str) -> Any:
        """Get the status and details of a call."""
        return self._client.get(f"/v1/voice/status/{call_id}")
