from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Optional, Set, List, Union

from ....utils.utils import _get_as_snowflake, _RawReprMixin

if TYPE_CHECKING:
    from typing_extensions import Self

    from .types import PollVoteActionEvent
    


__all__ = ('RawPollVoteActionEvent',
)

class RawPollVoteActionEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_poll_vote_add` or :func:`on_raw_poll_vote_remove`
    event.

    .. versionadded:: 2.4

    Attributes
    ----------
    user_id: :class:`int`
        The ID of the user that added or removed a vote.
    channel_id: :class:`int`
        The channel ID where the poll vote action took place.
    message_id: :class:`int`
        The message ID that contains the poll the user added or removed their vote on.
    guild_id: Optional[:class:`int`]
        The guild ID where the vote got added or removed, if applicable..
    answer_id: :class:`int`
        The poll answer's ID the user voted on.
    """

    __slots__ = ('user_id', 'channel_id', 'message_id', 'guild_id', 'answer_id')

    def __init__(self, data: PollVoteActionEvent) -> None:
        self.user_id: int = int(data['user_id'])
        self.channel_id: int = int(data['channel_id'])
        self.message_id: int = int(data['message_id'])
        self.guild_id: Optional[int] = _get_as_snowflake(data, 'guild_id')
        self.answer_id: int = int(data['answer_id'])