from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from ..client.activity.activity import create_activity
from ...utils.utils import MISSING, _get_as_snowflake, _RawReprMixin
from ...utils.enums import try_enum
from ..user.enums import Status
from ..client.status import ClientStatus

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..client.activity.activity import ActivityTypes
    from ..guild import Guild
    from ..state import ConnectionState
    from ..client.activity import PartialPresenceUpdate



__all__ = ('RawPresenceUpdateEvent',
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