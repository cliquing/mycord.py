
from __future__ import annotations

from typing import TYPE_CHECKING, Union

from ....utils.utils import _RawReprMixin



if TYPE_CHECKING:

    from ..member.member import Member
    #from .types import ThreadPayload
    from ...user.user import User
    from .types import GuildMemberRemoveEvent



__all__ = ('RawMemberRemoveEvent',
)

class RawMemberRemoveEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_member_remove` event.

    .. versionadded:: 2.0

    Attributes
    ----------
    user: Union[:class:`discord.User`, :class:`discord.Member`]
        The user that left the guild.
    guild_id: :class:`int`
        The ID of the guild the user left.
    """

    __slots__ = ('user', 'guild_id')

    def __init__(self, data: GuildMemberRemoveEvent, user: User, /) -> None:
        self.user: Union[User, Member] = user
        self.guild_id: int = int(data['guild_id'])