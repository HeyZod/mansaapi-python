from __future__ import annotations

from typing import Any, Optional


class MansaAPIError(Exception):
    """Raised when the Mansa API returns an error response."""

    def __init__(self, code: str, message: str, status: int, raw: Optional[Any] = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.raw = raw

    def __repr__(self) -> str:  # pragma: no cover
        return f"MansaAPIError(code={self.code!r}, status={self.status}, message={self.message!r})"
