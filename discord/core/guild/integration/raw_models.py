from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal, Optional, Set, List, Union

from ....utils.utils import _get_as_snowflake, _RawReprMixin
if TYPE_CHECKING:
    from typing_extensions import Self

    from ...gateway import IntegrationDeleteEvent
    
    from ...message.message import Message
    from ...emoji import PartialEmoji
    from ..member.member import Member
    from ...user.user import User
    from ...state.state import ConnectionState
    from ..guild import Guild




__all__ = ('RawIntegrationDeleteEvent',
)

class RawIntegrationDeleteEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_integration_delete` event.

    .. versionadded:: 2.0

    Attributes
    -----------
    integration_id: :class:`int`
        The ID of the integration that got deleted.
    application_id: Optional[:class:`int`]
        The ID of the bot/OAuth2 application for this deleted integration.
    guild_id: :class:`int`
        The guild ID where the integration got deleted.
    """

    __slots__ = ('integration_id', 'application_id', 'guild_id')

    def __init__(self, data: IntegrationDeleteEvent) -> None:
        self.integration_id: int = int(data['id'])
        self.guild_id: int = int(data['guild_id'])

        try:
            self.application_id: Optional[int] = int(
                data['application_id']  # pyright: ignore[reportTypedDictNotRequiredAccess]
            )
        except KeyError:
            self.application_id: Optional[int] = None
