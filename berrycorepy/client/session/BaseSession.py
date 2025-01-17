import abc
import datetime
import json
from enum import Enum
from http import HTTPStatus
from types import TracebackType
from typing import Final, Callable, Any, cast, Optional, Dict, AsyncGenerator, Type

from pydantic import ValidationError

from berrycorepy.client.client import Client
from berrycorepy.client.dangerous import PRODUCTION, DangerousAPIServer
from berrycorepy.exceptions import ClientDecodeError, DangerousAPIError
from berrycorepy.methods.base import DangerousType, DangerousMethod, Response
from berrycorepy.types.base import DangerousObject

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]
DEFAULT_TIMEOUT: Final[float] = 60.0

class BaseSession(abc.ABC):
    """
    This is base class for all HTTP sessions in aiogram.

    If you want to create your own session, you must inherit from this class.
    """

    def __init__(
        self,
        api: DangerousAPIServer = PRODUCTION,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """

        :param api: Dangerous Client API URL patterns
        :param json_loads: JSON loader
        :param json_dumps: JSON dumper
        :param timeout: Session scope request timeout
        """
        self.api = api
        self.json_loads = json_loads
        self.json_dumps = json_dumps
        self.timeout = timeout

    def check_response(
            self, client: Client, method: DangerousMethod[DangerousType], status_code: int, content: str
    ) -> Response[DangerousType]:
        """
        Check response status
        """
        try:
            json_data = self.json_loads(content)
        except Exception as e:
            # Handled error type can't be classified as specific error
            # in due to decoder can be customized and raise any exception

            raise ClientDecodeError("Failed to decode object", e, content)

        try:
            response_type = Response[method.__returning__]  # type: ignore
            response = response_type.model_validate(json_data, context={"client": client})
        except ValidationError as e:
            raise ClientDecodeError("Failed to deserialize object", e, json_data)

        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED and response.ok:
            return response

        description = cast(str, response.description)

        #todo if parameters := response.parameters:
        #     if parameters.retry_after:
        #         raise DangerousRetryAfter(
        #             method=method, message=description, retry_after=parameters.retry_after
        #         )
        #
        # if status_code == HTTPStatus.BAD_REQUEST:
        #     raise DangerousBadRequest(method=method, message=description)
        # if status_code == HTTPStatus.NOT_FOUND:
        #     raise DangerousNotFound(method=method, message=description)
        # if status_code == HTTPStatus.CONFLICT:
        #     raise DangerousConflictError(method=method, message=description)
        # if status_code == HTTPStatus.UNAUTHORIZED:
        #     raise DangerousUnauthorizedError(method=method, message=description)
        # if status_code == HTTPStatus.FORBIDDEN:
        #     raise DangerousForbiddenError(method=method, message=description)
        # if status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        #     raise DangerousEntityTooLarge(method=method, message=description)
        # if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        #     if "restart" in description:
        #         raise RestartingDangerous(method=method, message=description)
        #     raise DangerousServerError(method=method, message=description)

        raise DangerousAPIError(
            method=method,
            message=description,
        )

    @abc.abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """
        Close client session
        """
        pass

    @abc.abstractmethod
    async def make_request(
            self,
            client: Client,
            method: DangerousMethod[DangerousType],
            timeout: Optional[int] = None,
    ) -> DangerousType:  # pragma: no cover
        """
        Make request to Telegram Bot API

        :param client: Client instance
        :param method: Method instance
        :param timeout: Request timeout
        :return:
        :raise DangerousApiError:
        """
        pass

    @abc.abstractmethod
    async def stream_content(
            self,
            url: str,
            headers: Optional[Dict[str, Any]] = None,
            timeout: int = 30,
            chunk_size: int = 65536,
            raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        """
        Stream reader
        """
        yield b""

    def prepare_value(
            self,
            value: Any,
            client: Client,
            files: Dict[str, Any],
            _dumps_json: bool = True,
    ) -> Any:
        """
        Prepare value before send
        """
        if value is None:
            return None
        if isinstance(value, str):
            return value

  #TODO file attach      # if isinstance(value, InputFile):
        #     key = secrets.token_urlsafe(10)
        #     files[key] = value
        #     return f"attach://{key}"

        if isinstance(value, dict):
            value = {
                key: prepared_item
                for key, item in value.items()
                if (
                       prepared_item := self.prepare_value(
                           item, client=client, files=files, _dumps_json=False
                       )
                   )
                   is not None
            }
            if _dumps_json:
                return self.json_dumps(value)
            return value
        if isinstance(value, list):
            value = [
                prepared_item
                for item in value
                if (
                       prepared_item := self.prepare_value(
                           item, client=client, files=files, _dumps_json=False
                       )
                   )
                   is not None
            ]
            if _dumps_json:
                return self.json_dumps(value)
            return value
        if isinstance(value, datetime.timedelta):
            now = datetime.datetime.now()
            return str(round((now + value).timestamp()))
        if isinstance(value, datetime.datetime):
            return str(round(value.timestamp()))
        if isinstance(value, Enum):
            return self.prepare_value(value.value, client=client, files=files)
        if isinstance(value, DangerousObject):
            return self.prepare_value(
                value.model_dump(warnings=False),
                client=client,
                files=files,
                _dumps_json=_dumps_json,
            )
        if _dumps_json:
            return self.json_dumps(value)
        return value

    async def __call__(
            self,
            client: Client,
            method: DangerousMethod[DangerousType],
            timeout: Optional[int] = None,
    ) -> DangerousType:
        middleware = self.middleware.wrap_middlewares(self.make_request, timeout=timeout)
        return cast(DangerousType, await middleware(client, method))

    async def __aenter__(self) -> BaseSession:
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None:
        await self.close()