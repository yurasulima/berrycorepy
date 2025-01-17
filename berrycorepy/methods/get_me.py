from __future__ import annotations

from ..types import User
from .base import DangerousMethod


class GetMe(DangerousMethod[User]):
    """
    A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a :class:`berrycorepy.types.user.User` object.

    Source:
    """

    __returning__ = User
    __api_method__ = "getMe"