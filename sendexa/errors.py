from __future__ import annotations

from typing import Any, Optional


class SendexaError(Exception):
    """Raised for every API-level error returned by the Sendexa platform."""

    status: int
    code: str
    request_id: Optional[str]
    raw: Any

    def __init__(
        self,
        message: str,
        status: int,
        code: str,
        request_id: Optional[str] = None,
        raw: Any = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.request_id = request_id
        self.raw = raw

    def __repr__(self) -> str:
        return (
            f"SendexaError(status={self.status}, code={self.code!r}, "
            f"message={str(self)!r}, request_id={self.request_id!r})"
        )
