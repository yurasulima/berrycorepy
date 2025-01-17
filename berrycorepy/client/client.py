from typing import Any, Optional, T

from berrycorepy.client.session.BaseSession import BaseSession
from berrycorepy.methods.base import DangerousMethod


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
        """ #todo add page/bot


        if session is None:
            session = AiohttpSession()

    async def __call__(
            self, method: DangerousMethod[T], request_timeout: Optional[int] = None
    ) -> T:
        """
        Call API method

        :param method:
        :return:
        """
        return await self.session(self, method, timeout=request_timeout)

