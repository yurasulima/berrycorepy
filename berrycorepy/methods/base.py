from __future__ import annotations

from typing import TypeVar, Any, Generic, Generator, TYPE_CHECKING, ClassVar, Dict, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict

from berrycorepy.client.context_controller import ClientContextController
from ..types.response_parameters import ResponseParameters

if TYPE_CHECKING:
    from ..client.client import Client

DangerousType = TypeVar("DangerousType", bound=Any)

class Request(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    method: str

    data: Dict[str, Optional[Any]]
#todo    files: Optional[Dict[str, InputFile]]


class Response(BaseModel, Generic[DangerousType]):
    ok: bool
    result: Optional[DangerousType] = None
    description: Optional[str] = None
    error_code: Optional[int] = None
    parameters: Optional[ResponseParameters] = None



class DangerousMethod(ClientContextController, BaseModel, Generic[DangerousType], ABC):
    if TYPE_CHECKING:
        __returning__: ClassVar[type]
        __api_method__: ClassVar[str]
    else:

        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass

        @property
        @abstractmethod
        def __api_method__(self) -> str:
            pass

    async def emit(self, client: Client) -> DangerousType:
        return await client(self)

    def __await__(self) -> Generator[Any, None, DangerousType]:
        client = self._client
        if not client:
            raise RuntimeError(
                "This method is not mounted to a any client instance, please call it explicilty "
                "with client instance `await client(method)`\n"
                "or mount method to a client instance `method.as_(client)` "
                "and then call it `await method`"
            )
        return self.emit(client).__await__()