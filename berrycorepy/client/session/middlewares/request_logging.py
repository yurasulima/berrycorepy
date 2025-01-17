import logging
from typing import TYPE_CHECKING, Any, List, Optional, Type

from berrycorepy import loggers
from berrycorepy.methods.base import DangerousMethod
from berrycorepy.methods.base import Response, DangerousType

from .base import BaseRequestMiddleware, NextRequestMiddlewareType

if TYPE_CHECKING:
    from ...client import Client

logger = logging.getLogger(__name__)


class RequestLogging(BaseRequestMiddleware):
    def __init__(self, ignore_methods: Optional[List[Type[DangerousMethod[Any]]]] = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods if ignore_methods else []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[DangerousType],
        client: "Client",
        method: DangerousMethod[DangerousType],
    ) -> Response[DangerousType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by client id=%d",
                type(method).__name__,
                client.id,
            )
        return await make_request(client, method)