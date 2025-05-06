from __future__ import annotations
import datetime
from typing import TYPE_CHECKING, Optional, Tuple, Union

from .activity.activity import create_activity
from ...utils.utils import _get_as_snowflake, _RawReprMixin
from .status import ClientStatus
if TYPE_CHECKING:

    from .activity.activity import ActivityTypes
    from ..guild import Guild
    from ..state.state import ConnectionState
    from .activity import PartialPresenceUpdate
    from .types import TypingStartEvent
    from ..user import User
    from ..guild.member import Member



__all__ = ('RawPresenceUpdateEvent', 'RawTypingEvent',
)



class RawPresenceUpdateEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_presence_update` event.

    .. versionadded:: 2.5

    Attributes
    ----------
    user_id: :class:`int`
        The ID of the user that triggered the presence update.
    guild_id: Optional[:class:`int`]
        The guild ID for the users presence update. Could be ``None``.
    guild: Optional[:class:`Guild`]
        The guild associated with the presence update and user. Could be ``None``.
    client_status: :class:`ClientStatus`
        The :class:`~.ClientStatus` model which holds information about the status of the user on various clients.
    activities: Tuple[Union[:class:`BaseActivity`, :class:`Spotify`]]
        The activities the user is currently doing. Due to a Discord API limitation, a user's Spotify activity may not appear
        if they are listening to a song with a title longer than ``128`` characters. See :issue:`1738` for more information.
    """

    __slots__ = ('user_id', 'guild_id', 'guild', 'client_status', 'activities')

    def __init__(self, *, data: PartialPresenceUpdate, state: ConnectionState) -> None:
        self.user_id: int = int(data['user']['id'])
        self.client_status: ClientStatus = ClientStatus(status=data['status'], data=data['client_status'])
        self.activities: Tuple[ActivityTypes, ...] = tuple(create_activity(d, state) for d in data['activities'])
        self.guild_id: Optional[int] = _get_as_snowflake(data, 'guild_id')
        self.guild: Optional[Guild] = state._get_guild(self.guild_id)




class RawTypingEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_typing` event.

    .. versionadded:: 2.0

    Attributes
    ----------
    channel_id: :class:`int`
        The ID of the channel the user started typing in.
    user_id: :class:`int`
        The ID of the user that started typing.
    user: Optional[Union[:class:`discord.User`, :class:`discord.Member`]]
        The user that started typing, if they could be found in the internal cache.
    timestamp: :class:`datetime.datetime`
        When the typing started as an aware datetime in UTC.
    guild_id: Optional[:class:`int`]
        The ID of the guild the user started typing in, if applicable.
    """

    __slots__ = ('channel_id', 'user_id', 'user', 'timestamp', 'guild_id')

    def __init__(self, data: TypingStartEvent, /) -> None:
        self.channel_id: int = int(data['channel_id'])
        self.user_id: int = int(data['user_id'])
        self.user: Optional[Union[User, Member]] = None
        self.timestamp: datetime.datetime = datetime.datetime.fromtimestamp(data['timestamp'], tz=datetime.timezone.utc)
        self.guild_id: Optional[int] = _get_as_snowflake(data, 'guild_id')