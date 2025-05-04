from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal, Optional, Set, List, Union

from .enums import ReactionType
from ....utils.utils import _get_as_snowflake, _RawReprMixin
from ....utils.color import Colour
from ....utils.enums import try_enum

if TYPE_CHECKING:
    from typing_extensions import Self
    from ..types import (MessageReactionAddEvent, MessageReactionRemoveEvent,
        MessageReactionRemoveAllEvent as ReactionClearEvent,
        MessageReactionRemoveEmojiEvent as ReactionClearEmojiEvent,
    )

    from ...guild.member import Member
    from ...emoji import PartialEmoji

    ReactionActionEvent = Union[MessageReactionAddEvent, MessageReactionRemoveEvent]
    ReactionActionType = Literal['REACTION_ADD', 'REACTION_REMOVE']


__all__ = ('RawReactionActionEvent', 'RawReactionClearEvent', 'RawReactionClearEmojiEvent',
)

class RawReactionActionEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_reaction_add` or
    :func:`on_raw_reaction_remove` event.

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got or lost a reaction.
    user_id: :class:`int`
        The user ID who added the reaction or whose reaction was removed.
    channel_id: :class:`int`
        The channel ID where the reaction got added or removed.
    guild_id: Optional[:class:`int`]
        The guild ID where the reaction got added or removed, if applicable.
    emoji: :class:`PartialEmoji`
        The custom or unicode emoji being used.
    member: Optional[:class:`Member`]
        The member who added the reaction. Only available if ``event_type`` is ``REACTION_ADD`` and the reaction is inside a guild.

        .. versionadded:: 1.3
    message_author_id: Optional[:class:`int`]
        The author ID of the message being reacted to. Only available if ``event_type`` is ``REACTION_ADD``.

        .. versionadded:: 2.4
    event_type: :class:`str`
        The event type that triggered this action. Can be
        ``REACTION_ADD`` for reaction addition or
        ``REACTION_REMOVE`` for reaction removal.

        .. versionadded:: 1.3
    burst: :class:`bool`
        Whether the reaction was a burst reaction, also known as a "super reaction".

        .. versionadded:: 2.4
    burst_colours: List[:class:`Colour`]
        A list of colours used for burst reaction animation. Only available if ``burst`` is ``True``
        and if ``event_type`` is ``REACTION_ADD``.

        .. versionadded:: 2.0
    type: :class:`ReactionType`
        The type of the reaction.

        .. versionadded:: 2.4
    """

    __slots__ = (
        'message_id',
        'user_id',
        'channel_id',
        'guild_id',
        'emoji',
        'event_type',
        'member',
        'message_author_id',
        'burst',
        'burst_colours',
        'type',
    )

    def __init__(self, data: ReactionActionEvent, emoji: PartialEmoji, event_type: ReactionActionType) -> None:
        self.message_id: int = int(data['message_id'])
        self.channel_id: int = int(data['channel_id'])
        self.user_id: int = int(data['user_id'])
        self.emoji: PartialEmoji = emoji
        self.event_type: ReactionActionType = event_type
        self.member: Optional[Member] = None
        self.message_author_id: Optional[int] = _get_as_snowflake(data, 'message_author_id')
        self.burst: bool = data.get('burst', False)
        self.burst_colours: List[Colour] = [Colour.from_str(c) for c in data.get('burst_colours', [])]
        self.type: ReactionType = try_enum(ReactionType, data['type'])

        try:
            self.guild_id: Optional[int] = int(data['guild_id'])  # pyright: ignore[reportTypedDictNotRequiredAccess]
        except KeyError:
            self.guild_id: Optional[int] = None

    @property
    def burst_colors(self) -> List[Colour]:
        """An alias of :attr:`burst_colours`.

        .. versionadded:: 2.4
        """
        return self.burst_colours


class RawReactionClearEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_reaction_clear` event.

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got its reactions cleared.
    channel_id: :class:`int`
        The channel ID where the reactions got cleared.
    guild_id: Optional[:class:`int`]
        The guild ID where the reactions got cleared.
    """

    __slots__ = ('message_id', 'channel_id', 'guild_id')

    def __init__(self, data: ReactionClearEvent) -> None:
        self.message_id: int = int(data['message_id'])
        self.channel_id: int = int(data['channel_id'])

        try:
            self.guild_id: Optional[int] = int(data['guild_id'])  # pyright: ignore[reportTypedDictNotRequiredAccess]
        except KeyError:
            self.guild_id: Optional[int] = None


class RawReactionClearEmojiEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_reaction_clear_emoji` event.

    .. versionadded:: 1.3

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got its reactions cleared.
    channel_id: :class:`int`
        The channel ID where the reactions got cleared.
    guild_id: Optional[:class:`int`]
        The guild ID where the reactions got cleared.
    emoji: :class:`PartialEmoji`
        The custom or unicode emoji being removed.
    """

    __slots__ = ('message_id', 'channel_id', 'guild_id', 'emoji')

    def __init__(self, data: ReactionClearEmojiEvent, emoji: PartialEmoji) -> None:
        self.emoji: PartialEmoji = emoji
        self.message_id: int = int(data['message_id'])
        self.channel_id: int = int(data['channel_id'])

        try:
            self.guild_id: Optional[int] = int(data['guild_id'])  # pyright: ignore[reportTypedDictNotRequiredAccess]
        except KeyError:
            self.guild_id: Optional[int] = None
