from __future__ import annotations


from contextlib import asynccontextmanager
from types import TracebackType
from typing import Any, Optional, TypeVar, Type, AsyncIterator


from berrycorepy.types.User import User
from berrycorepy.methods import (
    DangerousMethod,
    GetMe
)
from berrycorepy.client.session.aiohttp import AiohttpSession
from berrycorepy.client.session.BaseSession import BaseSession
T = TypeVar("T")

class Client:
    def __init__(
            self,
            token: str,
            session: Optional[BaseSession] = None,
            **kwargs: Any,
    ) -> None:
        """
               Client class
               :param token: Dangerous API token `Obtained from ` 
        """ #todo add page/client


        if session is None:
            session = AiohttpSession()
        self.session = session
        self.__token = token
        self._me: Optional[User] = None

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None:
        await self.session.close()

    @property
    def token(self) -> str:
        return self.__token



    @asynccontextmanager
    async def context(self, auto_close: bool = True) -> AsyncIterator[Client]:
        """
        Generate client context

        :param auto_close: close session on exit
        :return:
        """
        try:
            yield self
        finally:
            if auto_close:
                await self.session.close()

    async def me(self) -> User:
        """
        Cached alias for getMe method

        :return:
        """
        if self._me is None:  # pragma: no cover
            self._me = await self.get_me()
        return self._me

    async def __call__(
            self, method: DangerousMethod[T], request_timeout: Optional[int] = None
    ) -> T:
        """
        Call API method

        :param method:
        :return:
        """
        return await self.session(self, method, timeout=request_timeout)


    def __hash__(self) -> int:
        """
        Get hash for the token

        :return:
        """
        return hash(self.__token)

    def __eq__(self, other: Any) -> bool:
        """
        Compare current client with another client instance

        :param other:
        :return:
        """
        if not isinstance(other, Client):
            return False
        return hash(self) == hash(other)



    async def get_me(
        self,
        request_timeout: Optional[int] = None,
    ) -> User:
        """
        A simple method for testing your client's authentication token. Requires no parameters. Returns basic information about the client in form of a :class:`berrycorepy.types.user.User` object.


        :param request_timeout: Request timeout
        :return: Returns basic information about the client in form of a :class:`berrycorepy.types.user.User` object.
        """

        call = GetMe()
        return await self(call, request_timeout=request_timeout)