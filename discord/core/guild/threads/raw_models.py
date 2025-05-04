from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal, Optional, Set, List, Union

from ....utils.utils import _get_as_snowflake, _RawReprMixin
from ....utils.enums import try_enum
from ..channel.enums import ChannelType

if TYPE_CHECKING:
    from typing_extensions import Self

    from ...gateway import (
        ThreadUpdateEvent,
        ThreadDeleteEvent,
        ThreadMembersUpdate,

    )
    from ...message.message import Message
    from ...emoji import PartialEmoji
    from ..member.member import Member
    #from .types import ThreadPayload
    from .threads import Thread
    from ...user.user import User
    from ...state.state import ConnectionState
    from ..guild import Guild



__all__ = ('RawThreadUpdateEvent', 'RawThreadDeleteEvent', 'RawThreadMembersUpdate',
)

class RawThreadUpdateEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_thread_update` event.

    .. versionadded:: 2.0

    Attributes
    ----------
    thread_id: :class:`int`
        The ID of the thread that was updated.
    thread_type: :class:`discord.ChannelType`
        The channel type of the updated thread.
    guild_id: :class:`int`
        The ID of the guild the thread is in.
    parent_id: :class:`int`
        The ID of the channel the thread belongs to.
    data: :class:`dict`
        The raw data given by the :ddocs:`gateway <topics/gateway-events#thread-update>`
    thread: Optional[:class:`discord.Thread`]
        The thread, if it could be found in the internal cache.
    """

    __slots__ = ('thread_id', 'thread_type', 'parent_id', 'guild_id', 'data', 'thread')

    def __init__(self, data: ThreadUpdateEvent) -> None:
        self.thread_id: int = int(data['id'])
        self.thread_type: ChannelType = try_enum(ChannelType, data['type'])
        self.guild_id: int = int(data['guild_id'])
        self.parent_id: int = int(data['parent_id'])
        self.data: ThreadUpdateEvent = data
        self.thread: Optional[Thread] = None


class RawThreadDeleteEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_thread_delete` event.

    .. versionadded:: 2.0

    Attributes
    ----------
    thread_id: :class:`int`
        The ID of the thread that was deleted.
    thread_type: :class:`discord.ChannelType`
        The channel type of the deleted thread.
    guild_id: :class:`int`
        The ID of the guild the thread was deleted in.
    parent_id: :class:`int`
        The ID of the channel the thread belonged to.
    thread: Optional[:class:`discord.Thread`]
        The thread, if it could be found in the internal cache.
    """

    __slots__ = ('thread_id', 'thread_type', 'parent_id', 'guild_id', 'thread')

    def __init__(self, data: ThreadDeleteEvent) -> None:
        self.thread_id: int = int(data['id'])
        self.thread_type: ChannelType = try_enum(ChannelType, data['type'])
        self.guild_id: int = int(data['guild_id'])
        self.parent_id: int = int(data['parent_id'])
        self.thread: Optional[Thread] = None

    @classmethod
    def _from_thread(cls, thread: Thread) -> Self:
        data: ThreadDeleteEvent = {
            'id': thread.id,
            'type': thread.type.value,
            'guild_id': thread.guild.id,
            'parent_id': thread.parent_id,
        }

        instance = cls(data)
        instance.thread = thread

        return instance


class RawThreadMembersUpdate(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_thread_member_remove` event.

    .. versionadded:: 2.0

    Attributes
    ----------
    thread_id: :class:`int`
        The ID of the thread that was updated.
    guild_id: :class:`int`
        The ID of the guild the thread is in.
    member_count: :class:`int`
        The approximate number of members in the thread. This caps at 50.
    data: :class:`dict`
        The raw data given by the :ddocs:`gateway <topics/gateway-events#thread-members-update>`.
    """

    __slots__ = ('thread_id', 'guild_id', 'member_count', 'data')

    def __init__(self, data: ThreadMembersUpdate) -> None:
        self.thread_id: int = int(data['id'])
        self.guild_id: int = int(data['guild_id'])
        self.member_count: int = int(data['member_count'])
        self.data: ThreadMembersUpdate = data
