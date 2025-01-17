from typing import Any, Optional

from berrycorepy.methods.base import DangerousMethod, DangerousType


class DetailedBerrycoreError(Exception):
    """
    Base exception for all berrycore errors with detailed message.
    """

    url: Optional[str] = None

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class BerrycoreError(Exception):
    """
    Base exception for all berrycore errors.
    """


class DangerousAPIError(DetailedBerrycoreError):
    """
    Base exception for all Telegram API errors.
    """

    label: str = "Dangerous server says"

    def __init__(
        self,
        method: DangerousMethod[DangerousType],
        message: str,
    ) -> None:
        super().__init__(message=message)
        self.method = method

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"



class ClientDecodeError(BerrycoreError):
    """
    Exception raised when client can't decode response. (Malformed response, etc.)
    """

    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )



class DangerousNetworkError(DangerousAPIError):
    """
    Base exception for all Dangerous network errors.
    """

    label = "HTTP Client says"
