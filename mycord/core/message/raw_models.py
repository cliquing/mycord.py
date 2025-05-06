from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional, Set, List, Union

from ...utils.utils import _RawReprMixin

if TYPE_CHECKING:


    from .types import MessageDeleteEvent, MessageDeleteBulkEvent, MessageReactionAddEvent, MessageReactionRemoveEvent, MessageUpdateEvent
    
    from .messages import Message

    ReactionActionEvent = Union[MessageReactionAddEvent, MessageReactionRemoveEvent]
    ReactionActionType = Literal['REACTION_ADD', 'REACTION_REMOVE']


__all__ = ('RawMessageDeleteEvent', 'RawMessageDeleteBulkEvent', 'RawMessageUpdateEvent',
)

class RawMessageDeleteEvent(_RawReprMixin):
    """Represents the event payload for a :func:`on_raw_message_delete` event.

    Attributes
    ------------
    channel_id: :class:`int`
        The channel ID where the deletion took place.
    guild_id: Optional[:class:`int`]
        The guild ID where the deletion took place, if applicable.
    message_id: :class:`int`
        The message ID that got deleted.
    cached_message: Optional[:class:`Message`]
        The cached message, if found in the internal message cache.
    """

    __slots__ = ('message_id', 'channel_id', 'guild_id', 'cached_message')

    def __init__(self, data: MessageDeleteEvent) -> None:
        self.message_id: int = int(data['id'])
        self.channel_id: int = int(data['channel_id'])
        self.cached_message: Optional[Message] = None
        try:
            self.guild_id: Optional[int] = int(data['guild_id'])  # pyright: ignore[reportTypedDictNotRequiredAccess]
        except KeyError:
            self.guild_id: Optional[int] = None


class RawMessageDeleteBulkEvent(_RawReprMixin):
    """Represents the event payload for a :func:`on_raw_bulk_message_delete` event.

    Attributes
    -----------
    message_ids: Set[:class:`int`]
        A :class:`set` of the message IDs that were deleted.
    channel_id: :class:`int`
        The channel ID where the message got deleted.
    guild_id: Optional[:class:`int`]
        The guild ID where the message got deleted, if applicable.
    cached_messages: List[:class:`Message`]
        The cached messages, if found in the internal message cache.
    """

    __slots__ = ('message_ids', 'channel_id', 'guild_id', 'cached_messages')

    def __init__(self, data: MessageDeleteBulkEvent) -> None:
        self.message_ids: Set[int] = {int(x) for x in data.get('ids', [])}
        self.channel_id: int = int(data['channel_id'])
        self.cached_messages: List[Message] = []

        try:
            self.guild_id: Optional[int] = int(data['guild_id'])  # pyright: ignore[reportTypedDictNotRequiredAccess]
        except KeyError:
            self.guild_id: Optional[int] = None


class RawMessageUpdateEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_message_edit` event.

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got updated.
    channel_id: :class:`int`
        The channel ID where the update took place.

        .. versionadded:: 1.3
    guild_id: Optional[:class:`int`]
        The guild ID where the message got updated, if applicable.

        .. versionadded:: 1.7

    data: :class:`dict`
        The raw data given by the :ddocs:`gateway <topics/gateway-events#message-update>`
    cached_message: Optional[:class:`Message`]
        The cached message, if found in the internal message cache. Represents the message before
        it is modified by the data in :attr:`RawMessageUpdateEvent.data`.
    message: :class:`Message`
        The updated message.

        .. versionadded:: 2.5
    """

    __slots__ = ('message_id', 'channel_id', 'guild_id', 'data', 'cached_message', 'message')

    def __init__(self, data: MessageUpdateEvent, message: Message) -> None:
        self.message_id: int = message.id
        self.channel_id: int = message.channel.id
        self.data: MessageUpdateEvent = data
        self.message: Message = message
        self.cached_message: Optional[Message] = None

        self.guild_id: Optional[int] = message.guild.id if message.guild else None
