from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .base import DangerousObject


class ResponseParameters(DangerousObject):
    """
    Describes why a request was unsuccessful.

    Source:
    """  # todo add description

    retry_after: Optional[int] = None
    """*Optional*. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
                __pydantic__self__,
                *,
                retry_after: Optional[int] = None,
                **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                retry_after=retry_after, **__pydantic_kwargs
            )
