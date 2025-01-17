from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from berrycorepy.methods.base import DangerousType, DangerousMethod, Response

if TYPE_CHECKING:
    from ...client import Client


class NextRequestMiddlewareType(Protocol[DangerousType]):  # pragma: no cover
    async def __call__(
        self,
        client: "Client",
        method: DangerousMethod[DangerousType],
    ) -> Response[DangerousType]:
        pass


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[DangerousType],
        client: "Client",
        method: DangerousMethod[DangerousType],
    ) -> Response[DangerousType]:
        pass


class BaseRequestMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[DangerousType],
        client: "Client",
        method: DangerousMethod[DangerousType],
    ) -> Response[DangerousType]:
        """
        Execute middleware

        :param make_request: Wrapped make_request in middlewares chain
        :param client: client for request making
        :param method: Request method (Subclass of :class:`aiogram.methods.base.DangerousMethod`)

        :return: :class:`aiogram.methods.Response`
        """
        pass