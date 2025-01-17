
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union


@dataclass(frozen=True)
class DangerousAPIServer:
    """
    Base config for API Endpoints
    """

    base: str
    """Base URL"""
    file: str
    """Files URL"""

    def api_url(self, token: str, method: str) -> str:
        """
        Generate URL for API methods

        :param token: Client token
        :param method: API method name (case insensitive)
        :return: URL
        """
        return self.base.format(token=token, method=method)

    def file_url(self, token: str, path: Union[str, Path]) -> str:
        """
        Generate URL for downloading files

        :param token: Client token
        :param path: file path
        :return: URL
        """
        return self.file.format(token=token, path=path)

    @classmethod
    def from_base(cls, base: str, **kwargs: Any) -> "DangerousAPIServer":
        """
        Use this method to auto-generate DangerousAPIServer instance from base URL

        :param base: Base URL
        :return: instance of :class:`DangerousAPIServer`
        """
        base = base.rstrip("/")
        return cls(
            base=f"{base}/client{{token}}/{{method}}",
            file=f"{base}/file/client{{token}}/{{path}}",
            **kwargs,
        )

PRODUCTION = DangerousAPIServer(
    base="https://mblueberry.fun/api/client{token}/{method}",
    file="https://mblueberry.fun/api/file/client{token}/{path}",
)
