from __future__ import annotations

from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    NamedTuple,
    Optional,
    TYPE_CHECKING,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
)
import datetime

import discord.abc
from .scheduled_event import ScheduledEvent
from .permissions import PermissionOverwrite, Permissions
from ..enums import (
    ChannelType,
    ForumLayoutType,
    ForumOrderType,
    PrivacyLevel,
    try_enum,
    VideoQualityMode,
    EntityType,
    VoiceChannelEffectAnimationType,
)
from .mixins import Hashable
from . import utils
from .utils import MISSING
from .asset import Asset
from .errors import ClientException
from .stage_instance import StageInstance
from .threads import Thread
from .partial_emoji import _EmojiTag, PartialEmoji
from .flags import ChannelFlags, MessageFlags
from .http import handle_message_parameters
from .object import Object
from .soundboard import BaseSoundboardSound, SoundboardDefaultSound

__all__ = (
    'TextChannel',
    'VoiceChannel',
    'StageChannel',
    'DMChannel',
    'CategoryChannel',
    'ForumTag',
    'ForumChannel',
    'GroupChannel',
    'PartialMessageable',
    'VoiceChannelEffect',
    'VoiceChannelSoundEffect',
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from .types.threads import ThreadArchiveDuration
    from .role import Role
    from .member import Member, VoiceState
    from .abc import Snowflake, SnowflakeTime
    from .embeds import Embed
    from .message import Message, PartialMessage, EmojiInputType
    from .mentions import AllowedMentions
    from .webhook import Webhook
    from .state import ConnectionState
    from .sticker import GuildSticker, StickerItem
    from .file import File
    from .core.user.user import ClientUser, User, BaseUser
    from .guild import Guild, GuildChannel as GuildChannelType
    from .ui.view import View
    from .types.channel import (
        TextChannel as TextChannelPayload,
        NewsChannel as NewsChannelPayload,
        VoiceChannel as VoiceChannelPayload,
        StageChannel as StageChannelPayload,
        DMChannel as DMChannelPayload,
        CategoryChannel as CategoryChannelPayload,
        GroupDMChannel as GroupChannelPayload,
        ForumChannel as ForumChannelPayload,
        MediaChannel as MediaChannelPayload,
        ForumTag as ForumTagPayload,
        VoiceChannelEffect as VoiceChannelEffectPayload,
    )
    from .types.snowflake import SnowflakeList
    from .types.soundboard import BaseSoundboardSound as BaseSoundboardSoundPayload
    from .soundboard import SoundboardSound

    OverwriteKeyT = TypeVar('OverwriteKeyT', Role, BaseUser, Object, Union[Role, Member, Object])




def _guild_channel_factory(channel_type: int):
    value = try_enum(ChannelType, channel_type)
    if value is ChannelType.text:
        return TextChannel, value
    elif value is ChannelType.voice:
        return VoiceChannel, value
    elif value is ChannelType.category:
        return CategoryChannel, value
    elif value is ChannelType.news:
        return TextChannel, value
    elif value is ChannelType.stage_voice:
        return StageChannel, value
    elif value is ChannelType.forum:
        return ForumChannel, value
    elif value is ChannelType.media:
        return ForumChannel, value
    else:
        return None, value


def _channel_factory(channel_type: int):
    cls, value = _guild_channel_factory(channel_type)
    if value is ChannelType.private:
        return DMChannel, value
    elif value is ChannelType.group:
        return GroupChannel, value
    else:
        return cls, value


def _threaded_channel_factory(channel_type: int):
    cls, value = _channel_factory(channel_type)
    if value in (ChannelType.private_thread, ChannelType.public_thread, ChannelType.news_thread):
        return Thread, value
    return cls, value


def _threaded_guild_channel_factory(channel_type: int):
    cls, value = _guild_channel_factory(channel_type)
    if value in (ChannelType.private_thread, ChannelType.public_thread, ChannelType.news_thread):
        return Thread, value
    return cls, value

class CategoryChannel(discord.abc.GuildChannel, Hashable):
    """Represents a Discord channel category.

    These are useful to group channels to logical compartments.

    .. container:: operations

        .. describe:: x == y

            Checks if two channels are equal.

        .. describe:: x != y

            Checks if two channels are not equal.

        .. describe:: hash(x)

            Returns the category's hash.

        .. describe:: str(x)

            Returns the category's name.

    Attributes
    -----------
    name: :class:`str`
        The category name.
    guild: :class:`Guild`
        The guild the category belongs to.
    id: :class:`int`
        The category channel ID.
    position: :class:`int`
        The position in the category list. This is a number that starts at 0. e.g. the
        top category is position 0.
    nsfw: :class:`bool`
        If the channel is marked as "not safe for work".

        .. note::

            To check if the channel or the guild of that channel are marked as NSFW, consider :meth:`is_nsfw` instead.
    """

    __slots__ = ('name', 'id', 'guild', 'nsfw', '_state', 'position', '_overwrites', 'category_id')

    def __init__(self, *, state: ConnectionState, guild: Guild, data: CategoryChannelPayload):
        self._state: ConnectionState = state
        self.id: int = int(data['id'])
        self._update(guild, data)

    def __repr__(self) -> str:
        return f'<CategoryChannel id={self.id} name={self.name!r} position={self.position} nsfw={self.nsfw}>'

    def _update(self, guild: Guild, data: CategoryChannelPayload) -> None:
        self.guild: Guild = guild
        self.name: str = data['name']
        self.category_id: Optional[int] = utils._get_as_snowflake(data, 'parent_id')
        self.nsfw: bool = data.get('nsfw', False)
        self.position: int = data['position']
        self._fill_overwrites(data)

    @property
    def _sorting_bucket(self) -> int:
        return ChannelType.category.value

    @property
    def _scheduled_event_entity_type(self) -> Optional[EntityType]:
        return None

    @property
    def type(self) -> Literal[ChannelType.category]:
        """:class:`ChannelType`: The channel's Discord type."""
        return ChannelType.category

    def is_nsfw(self) -> bool:
        """:class:`bool`: Checks if the category is NSFW."""
        return self.nsfw

    @utils.copy_doc(discord.abc.GuildChannel.clone)
    async def clone(
        self,
        *,
        name: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        reason: Optional[str] = None,
    ) -> CategoryChannel:
        return await self._clone_impl({'nsfw': self.nsfw}, name=name, reason=reason)

    @overload
    async def edit(self) -> None:
        ...

    @overload
    async def edit(self, *, position: int, reason: Optional[str] = ...) -> None:
        ...

    @overload
    async def edit(
        self,
        *,
        name: str = ...,
        position: int = ...,
        nsfw: bool = ...,
        overwrites: Mapping[OverwriteKeyT, PermissionOverwrite] = ...,
        reason: Optional[str] = ...,
    ) -> CategoryChannel:
        ...

    async def edit(self, *, reason: Optional[str] = None, **options: Any) -> Optional[CategoryChannel]:
        """|coro|

        Edits the channel.

        You must have :attr:`~Permissions.manage_channels` to do this.

        .. versionchanged:: 1.3
            The ``overwrites`` keyword-only parameter was added.

        .. versionchanged:: 2.0
            Edits are no longer in-place, the newly edited channel is returned instead.

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` or
            :exc:`ValueError` instead of ``InvalidArgument``.

        Parameters
        ----------
        name: :class:`str`
            The new category's name.
        position: :class:`int`
            The new category's position.
        nsfw: :class:`bool`
            To mark the category as NSFW or not.
        reason: Optional[:class:`str`]
            The reason for editing this category. Shows up on the audit log.
        overwrites: :class:`Mapping`
            A :class:`Mapping` of target (either a role or a member) to
            :class:`PermissionOverwrite` to apply to the channel.

        Raises
        ------
        ValueError
            If position is less than 0 or greater than the number of categories.
        TypeError
            The overwrite information is not in proper form.
        Forbidden
            You do not have permissions to edit the category.
        HTTPException
            Editing the category failed.

        Returns
        --------
        Optional[:class:`.CategoryChannel`]
            The newly edited category channel. If the edit was only positional
            then ``None`` is returned instead.
        """

        payload = await self._edit(options, reason=reason)
        if payload is not None:
            # the payload will always be the proper channel payload
            return self.__class__(state=self._state, guild=self.guild, data=payload)  # type: ignore

    @utils.copy_doc(discord.abc.GuildChannel.move)
    async def move(self, **kwargs: Any) -> None:
        kwargs.pop('category', None)
        await super().move(**kwargs)

    @property
    def channels(self) -> List[GuildChannelType]:
        """List[:class:`abc.GuildChannel`]: Returns the channels that are under this category.

        These are sorted by the official Discord UI, which places voice channels below the text channels.
        """

        def comparator(channel):
            return (not isinstance(channel, TextChannel), channel.position)

        ret = [c for c in self.guild.channels if c.category_id == self.id]
        ret.sort(key=comparator)
        return ret

    @property
    def text_channels(self) -> List[TextChannel]:
        """List[:class:`TextChannel`]: Returns the text channels that are under this category."""
        ret = [c for c in self.guild.channels if c.category_id == self.id and isinstance(c, TextChannel)]
        ret.sort(key=lambda c: (c.position, c.id))
        return ret

    @property
    def voice_channels(self) -> List[VoiceChannel]:
        """List[:class:`VoiceChannel`]: Returns the voice channels that are under this category."""
        ret = [c for c in self.guild.channels if c.category_id == self.id and isinstance(c, VoiceChannel)]
        ret.sort(key=lambda c: (c.position, c.id))
        return ret

    @property
    def stage_channels(self) -> List[StageChannel]:
        """List[:class:`StageChannel`]: Returns the stage channels that are under this category.

        .. versionadded:: 1.7
        """
        ret = [c for c in self.guild.channels if c.category_id == self.id and isinstance(c, StageChannel)]
        ret.sort(key=lambda c: (c.position, c.id))
        return ret

    @property
    def forums(self) -> List[ForumChannel]:
        """List[:class:`ForumChannel`]: Returns the forum channels that are under this category.

        .. versionadded:: 2.4
        """
        r = [c for c in self.guild.channels if c.category_id == self.id and isinstance(c, ForumChannel)]
        r.sort(key=lambda c: (c.position, c.id))
        return r

    async def create_text_channel(self, name: str, **options: Any) -> TextChannel:
        """|coro|

        A shortcut method to :meth:`Guild.create_text_channel` to create a :class:`TextChannel` in the category.

        Returns
        -------
        :class:`TextChannel`
            The channel that was just created.
        """
        return await self.guild.create_text_channel(name, category=self, **options)

    async def create_voice_channel(self, name: str, **options: Any) -> VoiceChannel:
        """|coro|

        A shortcut method to :meth:`Guild.create_voice_channel` to create a :class:`VoiceChannel` in the category.

        Returns
        -------
        :class:`VoiceChannel`
            The channel that was just created.
        """
        return await self.guild.create_voice_channel(name, category=self, **options)

    async def create_stage_channel(self, name: str, **options: Any) -> StageChannel:
        """|coro|

        A shortcut method to :meth:`Guild.create_stage_channel` to create a :class:`StageChannel` in the category.

        .. versionadded:: 1.7

        Returns
        -------
        :class:`StageChannel`
            The channel that was just created.
        """
        return await self.guild.create_stage_channel(name, category=self, **options)

    async def create_forum(self, name: str, **options: Any) -> ForumChannel:
        """|coro|

        A shortcut method to :meth:`Guild.create_forum` to create a :class:`ForumChannel` in the category.

        .. versionadded:: 2.0

        Returns
        --------
        :class:`ForumChannel`
            The channel that was just created.
        """
        return await self.guild.create_forum(name, category=self, **options)


class ForumTag(Hashable):
    """Represents a forum tag that can be applied to a thread within a :class:`ForumChannel`.

    .. versionadded:: 2.1

    .. container:: operations

        .. describe:: x == y

            Checks if two forum tags are equal.

        .. describe:: x != y

            Checks if two forum tags are not equal.

        .. describe:: hash(x)

            Returns the forum tag's hash.

        .. describe:: str(x)

            Returns the forum tag's name.


    Attributes
    -----------
    id: :class:`int`
        The ID of the tag. If this was manually created then the ID will be ``0``.
    name: :class:`str`
        The name of the tag. Can only be up to 20 characters.
    moderated: :class:`bool`
        Whether this tag can only be added or removed by a moderator with
        the :attr:`~Permissions.manage_threads` permission.
    emoji: Optional[:class:`PartialEmoji`]
        The emoji that is used to represent this tag.
        Note that if the emoji is a custom emoji, it will *not* have name information.
    """

    __slots__ = ('name', 'id', 'moderated', 'emoji')

    def __init__(self, *, name: str, emoji: Optional[EmojiInputType] = None, moderated: bool = False) -> None:
        self.name: str = name
        self.id: int = 0
        self.moderated: bool = moderated
        self.emoji: Optional[PartialEmoji] = None
        if isinstance(emoji, _EmojiTag):
            self.emoji = emoji._to_partial()
        elif isinstance(emoji, str):
            self.emoji = PartialEmoji.from_str(emoji)
        elif emoji is not None:
            raise TypeError(f'emoji must be a Emoji, PartialEmoji, str or None not {emoji.__class__.__name__}')

    @classmethod
    def from_data(cls, *, state: ConnectionState, data: ForumTagPayload) -> Self:
        self = cls.__new__(cls)
        self.name = data['name']
        self.id = int(data['id'])
        self.moderated = data.get('moderated', False)

        emoji_name = data['emoji_name'] or ''
        emoji_id = utils._get_as_snowflake(data, 'emoji_id') or None  # Coerce 0 -> None
        if not emoji_name and not emoji_id:
            self.emoji = None
        else:
            self.emoji = PartialEmoji.with_state(state=state, name=emoji_name, id=emoji_id)
        return self

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            'name': self.name,
            'moderated': self.moderated,
        }
        if self.emoji is not None:
            payload.update(self.emoji._to_forum_tag_payload())
        else:
            payload.update(emoji_id=None, emoji_name=None)

        if self.id:
            payload['id'] = self.id

        return payload

    def __repr__(self) -> str:
        return f'<ForumTag id={self.id} name={self.name!r} emoji={self.emoji!r} moderated={self.moderated}>'

    def __str__(self) -> str:
        return self.name


class ForumChannel(discord.abc.GuildChannel, Hashable):
    """Represents a Discord guild forum channel.

    .. versionadded:: 2.0

    .. container:: operations

        .. describe:: x == y

            Checks if two forums are equal.

        .. describe:: x != y

            Checks if two forums are not equal.

        .. describe:: hash(x)

            Returns the forum's hash.

        .. describe:: str(x)

            Returns the forum's name.

    Attributes
    -----------
    name: :class:`str`
        The forum name.
    guild: :class:`Guild`
        The guild the forum belongs to.
    id: :class:`int`
        The forum ID.
    category_id: Optional[:class:`int`]
        The category channel ID this forum belongs to, if applicable.
    topic: Optional[:class:`str`]
        The forum's topic. ``None`` if it doesn't exist. Called "Guidelines" in the UI.
        Can be up to 4096 characters long.
    position: :class:`int`
        The position in the channel list. This is a number that starts at 0. e.g. the
        top channel is position 0.
    last_message_id: Optional[:class:`int`]
        The last thread ID that was created on this forum. This technically also
        coincides with the message ID that started the thread that was created.
        It may *not* point to an existing or valid thread or message.
    slowmode_delay: :class:`int`
        The number of seconds a member must wait between creating threads
        in this forum. A value of ``0`` denotes that it is disabled.
        Bots and users with :attr:`~Permissions.manage_channels` or
        :attr:`~Permissions.manage_messages` bypass slowmode.
    nsfw: :class:`bool`
        If the forum is marked as "not safe for work" or "age restricted".
    default_auto_archive_duration: :class:`int`
        The default auto archive duration in minutes for threads created in this forum.
    default_thread_slowmode_delay: :class:`int`
        The default slowmode delay in seconds for threads created in this forum.

        .. versionadded:: 2.1
    default_reaction_emoji: Optional[:class:`PartialEmoji`]
        The default reaction emoji for threads created in this forum to show in the
        add reaction button.

        .. versionadded:: 2.1
    default_layout: :class:`ForumLayoutType`
        The default layout for posts in this forum channel.
        Defaults to :attr:`ForumLayoutType.not_set`.

        .. versionadded:: 2.2
    default_sort_order: Optional[:class:`ForumOrderType`]
        The default sort order for posts in this forum channel.

        .. versionadded:: 2.3
    """

    __slots__ = (
        'name',
        'id',
        'guild',
        'topic',
        '_state',
        '_flags',
        '_type',
        'nsfw',
        'category_id',
        'position',
        'slowmode_delay',
        '_overwrites',
        'last_message_id',
        'default_auto_archive_duration',
        'default_thread_slowmode_delay',
        'default_reaction_emoji',
        'default_layout',
        'default_sort_order',
        '_available_tags',
        '_flags',
    )

    def __init__(self, *, state: ConnectionState, guild: Guild, data: Union[ForumChannelPayload, MediaChannelPayload]):
        self._state: ConnectionState = state
        self.id: int = int(data['id'])
        self._type: Literal[15, 16] = data['type']
        self._update(guild, data)

    def __repr__(self) -> str:
        attrs = [
            ('id', self.id),
            ('name', self.name),
            ('position', self.position),
            ('nsfw', self.nsfw),
            ('category_id', self.category_id),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    def _update(self, guild: Guild, data: Union[ForumChannelPayload, MediaChannelPayload]) -> None:
        self.guild: Guild = guild
        self.name: str = data['name']
        self.category_id: Optional[int] = utils._get_as_snowflake(data, 'parent_id')
        self.topic: Optional[str] = data.get('topic')
        self.position: int = data['position']
        self.nsfw: bool = data.get('nsfw', False)
        self.slowmode_delay: int = data.get('rate_limit_per_user', 0)
        self.default_auto_archive_duration: ThreadArchiveDuration = data.get('default_auto_archive_duration', 1440)
        self.last_message_id: Optional[int] = utils._get_as_snowflake(data, 'last_message_id')
        # This takes advantage of the fact that dicts are ordered since Python 3.7
        tags = [ForumTag.from_data(state=self._state, data=tag) for tag in data.get('available_tags', [])]
        self.default_thread_slowmode_delay: int = data.get('default_thread_rate_limit_per_user', 0)
        self.default_layout: ForumLayoutType = try_enum(ForumLayoutType, data.get('default_forum_layout', 0))
        self._available_tags: Dict[int, ForumTag] = {tag.id: tag for tag in tags}

        self.default_reaction_emoji: Optional[PartialEmoji] = None
        default_reaction_emoji = data.get('default_reaction_emoji')
        if default_reaction_emoji:
            self.default_reaction_emoji = PartialEmoji.with_state(
                state=self._state,
                id=utils._get_as_snowflake(default_reaction_emoji, 'emoji_id') or None,  # Coerce 0 -> None
                name=default_reaction_emoji.get('emoji_name') or '',
            )

        self.default_sort_order: Optional[ForumOrderType] = None
        default_sort_order = data.get('default_sort_order')
        if default_sort_order is not None:
            self.default_sort_order = try_enum(ForumOrderType, default_sort_order)

        self._flags: int = data.get('flags', 0)
        self._fill_overwrites(data)

    @property
    def type(self) -> Literal[ChannelType.forum, ChannelType.media]:
        """:class:`ChannelType`: The channel's Discord type."""
        if self._type == 16:
            return ChannelType.media
        return ChannelType.forum

    @property
    def _sorting_bucket(self) -> int:
        return ChannelType.text.value

    @property
    def members(self) -> List[Member]:
        """List[:class:`Member`]: Returns all members that can see this channel.

        .. versionadded:: 2.5
        """
        return [m for m in self.guild.members if self.permissions_for(m).read_messages]

    @property
    def _scheduled_event_entity_type(self) -> Optional[EntityType]:
        return None

    @utils.copy_doc(discord.abc.GuildChannel.permissions_for)
    def permissions_for(self, obj: Union[Member, Role], /) -> Permissions:
        base = super().permissions_for(obj)
        self._apply_implicit_permissions(base)

        # text channels do not have voice related permissions
        denied = Permissions.voice()
        base.value &= ~denied.value
        return base

    def get_thread(self, thread_id: int, /) -> Optional[Thread]:
        """Returns a thread with the given ID.

        .. note::

            This does not always retrieve archived threads, as they are not retained in the internal
            cache. Use :func:`Guild.fetch_channel` instead.

        .. versionadded:: 2.2

        Parameters
        -----------
        thread_id: :class:`int`
            The ID to search for.

        Returns
        --------
        Optional[:class:`Thread`]
            The returned thread or ``None`` if not found.
        """
        thread = self.guild.get_thread(thread_id)
        if thread is not None and thread.parent_id == self.id:
            return thread
        return None

    @property
    def threads(self) -> List[Thread]:
        """List[:class:`Thread`]: Returns all the threads that you can see."""
        return [thread for thread in self.guild._threads.values() if thread.parent_id == self.id]

    @property
    def flags(self) -> ChannelFlags:
        """:class:`ChannelFlags`: The flags associated with this thread.

        .. versionadded:: 2.1
        """
        return ChannelFlags._from_value(self._flags)

    @property
    def available_tags(self) -> Sequence[ForumTag]:
        """Sequence[:class:`ForumTag`]: Returns all the available tags for this forum.

        .. versionadded:: 2.1
        """
        return utils.SequenceProxy(self._available_tags.values())

    def get_tag(self, tag_id: int, /) -> Optional[ForumTag]:
        """Returns the tag with the given ID.

        .. versionadded:: 2.1

        Parameters
        ----------
        tag_id: :class:`int`
            The ID to search for.

        Returns
        -------
        Optional[:class:`ForumTag`]
            The tag with the given ID, or ``None`` if not found.
        """
        return self._available_tags.get(tag_id)

    def is_nsfw(self) -> bool:
        """:class:`bool`: Checks if the forum is NSFW."""
        return self.nsfw

    def is_media(self) -> bool:
        """:class:`bool`: Checks if the channel is a media channel.

        .. versionadded:: 2.4
        """
        return self._type == ChannelType.media.value

    @utils.copy_doc(discord.abc.GuildChannel.clone)
    async def clone(
        self,
        *,
        name: Optional[str] = None,
        category: Optional[CategoryChannel],
        reason: Optional[str] = None,
    ) -> ForumChannel:
        base = {
            'topic': self.topic,
            'rate_limit_per_user': self.slowmode_delay,
            'nsfw': self.nsfw,
            'default_auto_archive_duration': self.default_auto_archive_duration,
            'available_tags': [tag.to_dict() for tag in self.available_tags],
            'default_thread_rate_limit_per_user': self.default_thread_slowmode_delay,
        }
        if self.default_sort_order:
            base['default_sort_order'] = self.default_sort_order.value
        if self.default_reaction_emoji:
            base['default_reaction_emoji'] = self.default_reaction_emoji._to_forum_tag_payload()
        if not self.is_media() and self.default_layout:
            base['default_forum_layout'] = self.default_layout.value

        return await self._clone_impl(
            base,
            name=name,
            category=category,
            reason=reason,
        )

    @overload
    async def edit(self) -> None:
        ...

    @overload
    async def edit(self, *, position: int, reason: Optional[str] = ...) -> None:
        ...

    @overload
    async def edit(
        self,
        *,
        reason: Optional[str] = ...,
        name: str = ...,
        topic: str = ...,
        position: int = ...,
        nsfw: bool = ...,
        sync_permissions: bool = ...,
        category: Optional[CategoryChannel] = ...,
        slowmode_delay: int = ...,
        default_auto_archive_duration: ThreadArchiveDuration = ...,
        type: ChannelType = ...,
        overwrites: Mapping[OverwriteKeyT, PermissionOverwrite] = ...,
        available_tags: Sequence[ForumTag] = ...,
        default_thread_slowmode_delay: int = ...,
        default_reaction_emoji: Optional[EmojiInputType] = ...,
        default_layout: ForumLayoutType = ...,
        default_sort_order: ForumOrderType = ...,
        require_tag: bool = ...,
    ) -> ForumChannel:
        ...

    async def edit(self, *, reason: Optional[str] = None, **options: Any) -> Optional[ForumChannel]:
        """|coro|

        Edits the forum.

        You must have :attr:`~Permissions.manage_channels` to do this.

        Parameters
        ----------
        name: :class:`str`
            The new forum name.
        topic: :class:`str`
            The new forum's topic.
        position: :class:`int`
            The new forum's position.
        nsfw: :class:`bool`
            To mark the forum as NSFW or not.
        sync_permissions: :class:`bool`
            Whether to sync permissions with the forum's new or pre-existing
            category. Defaults to ``False``.
        category: Optional[:class:`CategoryChannel`]
            The new category for this forum. Can be ``None`` to remove the
            category.
        slowmode_delay: :class:`int`
            Specifies the slowmode rate limit for user in this forum, in seconds.
            A value of ``0`` disables slowmode. The maximum value possible is ``21600``.
        type: :class:`ChannelType`
            Change the type of this text forum. Currently, only conversion between
            :attr:`ChannelType.text` and :attr:`ChannelType.news` is supported. This
            is only available to guilds that contain ``NEWS`` in :attr:`Guild.features`.
        reason: Optional[:class:`str`]
            The reason for editing this forum. Shows up on the audit log.
        overwrites: :class:`Mapping`
            A :class:`Mapping` of target (either a role or a member) to
            :class:`PermissionOverwrite` to apply to the forum.
        default_auto_archive_duration: :class:`int`
            The new default auto archive duration in minutes for threads created in this channel.
            Must be one of ``60``, ``1440``, ``4320``, or ``10080``.
        available_tags: Sequence[:class:`ForumTag`]
            The new available tags for this forum.

            .. versionadded:: 2.1
        default_thread_slowmode_delay: :class:`int`
            The new default slowmode delay for threads in this channel.

            .. versionadded:: 2.1
        default_reaction_emoji: Optional[Union[:class:`Emoji`, :class:`PartialEmoji`, :class:`str`]]
            The new default reaction emoji for threads in this channel.

            .. versionadded:: 2.1
        default_layout: :class:`ForumLayoutType`
            The new default layout for posts in this forum.

            .. versionadded:: 2.2
        default_sort_order: Optional[:class:`ForumOrderType`]
            The new default sort order for posts in this forum.

            .. versionadded:: 2.3
        require_tag: :class:`bool`
            Whether to require a tag for threads in this channel or not.

            .. versionadded:: 2.1

        Raises
        ------
        ValueError
            The new ``position`` is less than 0 or greater than the number of channels.
        TypeError
            The permission overwrite information is not in proper form or a type
            is not the expected type.
        Forbidden
            You do not have permissions to edit the forum.
        HTTPException
            Editing the forum failed.

        Returns
        --------
        Optional[:class:`.ForumChannel`]
            The newly edited forum channel. If the edit was only positional
            then ``None`` is returned instead.
        """

        try:
            tags: Sequence[ForumTag] = options.pop('available_tags')
        except KeyError:
            pass
        else:
            options['available_tags'] = [tag.to_dict() for tag in tags]

        try:
            default_reaction_emoji: Optional[EmojiInputType] = options.pop('default_reaction_emoji')
        except KeyError:
            pass
        else:
            if default_reaction_emoji is None:
                options['default_reaction_emoji'] = None
            elif isinstance(default_reaction_emoji, _EmojiTag):
                options['default_reaction_emoji'] = default_reaction_emoji._to_partial()._to_forum_tag_payload()
            elif isinstance(default_reaction_emoji, str):
                options['default_reaction_emoji'] = PartialEmoji.from_str(default_reaction_emoji)._to_forum_tag_payload()

        try:
            require_tag = options.pop('require_tag')
        except KeyError:
            pass
        else:
            flags = self.flags
            flags.require_tag = require_tag
            options['flags'] = flags.value

        try:
            layout = options.pop('default_layout')
        except KeyError:
            pass
        else:
            if not isinstance(layout, ForumLayoutType):
                raise TypeError(f'default_layout parameter must be a ForumLayoutType not {layout.__class__.__name__}')

            options['default_forum_layout'] = layout.value

        try:
            sort_order = options.pop('default_sort_order')
        except KeyError:
            pass
        else:
            if sort_order is None:
                options['default_sort_order'] = None
            else:
                if not isinstance(sort_order, ForumOrderType):
                    raise TypeError(
                        f'default_sort_order parameter must be a ForumOrderType not {sort_order.__class__.__name__}'
                    )

                options['default_sort_order'] = sort_order.value

        payload = await self._edit(options, reason=reason)
        if payload is not None:
            # the payload will always be the proper channel payload
            return self.__class__(state=self._state, guild=self.guild, data=payload)  # type: ignore

    async def create_tag(
        self,
        *,
        name: str,
        emoji: Optional[PartialEmoji] = None,
        moderated: bool = False,
        reason: Optional[str] = None,
    ) -> ForumTag:
        """|coro|

        Creates a new tag in this forum.

        You must have :attr:`~Permissions.manage_channels` to do this.

        Parameters
        ----------
        name: :class:`str`
            The name of the tag. Can only be up to 20 characters.
        emoji: Optional[Union[:class:`str`, :class:`PartialEmoji`]]
            The emoji to use for the tag.
        moderated: :class:`bool`
            Whether the tag can only be applied by moderators.
        reason: Optional[:class:`str`]
            The reason for creating this tag. Shows up on the audit log.

        Raises
        ------
        Forbidden
            You do not have permissions to create a tag in this forum.
        HTTPException
            Creating the tag failed.

        Returns
        -------
        :class:`ForumTag`
            The newly created tag.
        """

        prior = list(self._available_tags.values())
        result = ForumTag(name=name, emoji=emoji, moderated=moderated)
        prior.append(result)
        payload = await self._state.http.edit_channel(
            self.id, reason=reason, available_tags=[tag.to_dict() for tag in prior]
        )
        try:
            result.id = int(payload['available_tags'][-1]['id'])  # type: ignore
        except (KeyError, IndexError, ValueError):
            pass

        return result

    async def create_thread(
        self,
        *,
        name: str,
        auto_archive_duration: ThreadArchiveDuration = MISSING,
        slowmode_delay: Optional[int] = None,
        content: Optional[str] = None,
        tts: bool = False,
        embed: Embed = MISSING,
        embeds: Sequence[Embed] = MISSING,
        file: File = MISSING,
        files: Sequence[File] = MISSING,
        stickers: Sequence[Union[GuildSticker, StickerItem]] = MISSING,
        allowed_mentions: AllowedMentions = MISSING,
        mention_author: bool = MISSING,
        applied_tags: Sequence[ForumTag] = MISSING,
        view: View = MISSING,
        suppress_embeds: bool = False,
        reason: Optional[str] = None,
    ) -> ThreadWithMessage:
        """|coro|

        Creates a thread in this forum.

        This thread is a public thread with the initial message given. Currently in order
        to start a thread in this forum, the user needs :attr:`~discord.Permissions.send_messages`.

        You must send at least one of ``content``, ``embed``, ``embeds``, ``file``, ``files``,
        or ``view`` to create a thread in a forum, since forum channels must have a starter message.

        Parameters
        -----------
        name: :class:`str`
            The name of the thread.
        auto_archive_duration: :class:`int`
            The duration in minutes before a thread is automatically hidden from the channel list.
            If not provided, the channel's default auto archive duration is used.

            Must be one of ``60``, ``1440``, ``4320``, or ``10080``, if provided.
        slowmode_delay: Optional[:class:`int`]
            Specifies the slowmode rate limit for user in this channel, in seconds.
            The maximum value possible is ``21600``. By default no slowmode rate limit
            if this is ``None``.
        content: Optional[:class:`str`]
            The content of the message to send with the thread.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`~discord.Embed`
            The rich embed for the content.
        embeds: List[:class:`~discord.Embed`]
            A list of embeds to upload. Must be a maximum of 10.
        file: :class:`~discord.File`
            The file to upload.
        files: List[:class:`~discord.File`]
            A list of files to upload. Must be a maximum of 10.
        allowed_mentions: :class:`~discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`~discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`~discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`~discord.Client.allowed_mentions`
            are used instead.
        mention_author: :class:`bool`
            If set, overrides the :attr:`~discord.AllowedMentions.replied_user` attribute of ``allowed_mentions``.
        applied_tags: List[:class:`discord.ForumTag`]
            A list of tags to apply to the thread.
        view: :class:`discord.ui.View`
            A Discord UI View to add to the message.
        stickers: Sequence[Union[:class:`~discord.GuildSticker`, :class:`~discord.StickerItem`]]
            A list of stickers to upload. Must be a maximum of 3.
        suppress_embeds: :class:`bool`
            Whether to suppress embeds for the message. This sends the message without any embeds if set to ``True``.
        reason: :class:`str`
            The reason for creating a new thread. Shows up on the audit log.

        Raises
        -------
        Forbidden
            You do not have permissions to create a thread.
        HTTPException
            Starting the thread failed.
        ValueError
            The ``files`` or ``embeds`` list is not of the appropriate size.
        TypeError
            You specified both ``file`` and ``files``,
            or you specified both ``embed`` and ``embeds``.

        Returns
        --------
        Tuple[:class:`Thread`, :class:`Message`]
            The created thread with the created message.
            This is also accessible as a namedtuple with ``thread`` and ``message`` fields.
        """

        state = self._state
        previous_allowed_mention = state.allowed_mentions
        if stickers is MISSING:
            sticker_ids = MISSING
        else:
            sticker_ids: SnowflakeList = [s.id for s in stickers]

        if view and not hasattr(view, '__discord_ui_view__'):
            raise TypeError(f'view parameter must be View not {view.__class__.__name__}')

        if suppress_embeds:
            flags = MessageFlags._from_value(4)
        else:
            flags = MISSING

        content = str(content) if content else MISSING

        channel_payload = {
            'name': name,
            'auto_archive_duration': auto_archive_duration or self.default_auto_archive_duration,
            'rate_limit_per_user': slowmode_delay,
            'type': 11,  # Private threads don't seem to be allowed
        }

        if applied_tags is not MISSING:
            channel_payload['applied_tags'] = [str(tag.id) for tag in applied_tags]

        with handle_message_parameters(
            content=content,
            tts=tts,
            file=file,
            files=files,
            embed=embed,
            embeds=embeds,
            allowed_mentions=allowed_mentions,
            previous_allowed_mentions=previous_allowed_mention,
            mention_author=None if mention_author is MISSING else mention_author,
            stickers=sticker_ids,
            view=view,
            flags=flags,
            channel_payload=channel_payload,
        ) as params:
            # Circular import
            from .message import Message

            data = await state.http.start_thread_in_forum(self.id, params=params, reason=reason)
            thread = Thread(guild=self.guild, state=self._state, data=data)
            message = Message(state=self._state, channel=thread, data=data['message'])
            if view and not view.is_finished():
                self._state.store_view(view, message.id)

            return ThreadWithMessage(thread=thread, message=message)

    async def webhooks(self) -> List[Webhook]:
        """|coro|

        Gets the list of webhooks from this channel.

        You must have :attr:`~.Permissions.manage_webhooks` to do this.

        Raises
        -------
        Forbidden
            You don't have permissions to get the webhooks.

        Returns
        --------
        List[:class:`Webhook`]
            The webhooks for this channel.
        """

        from .webhook import Webhook

        data = await self._state.http.channel_webhooks(self.id)
        return [Webhook.from_state(d, state=self._state) for d in data]

    async def create_webhook(self, *, name: str, avatar: Optional[bytes] = None, reason: Optional[str] = None) -> Webhook:
        """|coro|

        Creates a webhook for this channel.

        You must have :attr:`~.Permissions.manage_webhooks` to do this.

        Parameters
        -------------
        name: :class:`str`
            The webhook's name.
        avatar: Optional[:class:`bytes`]
            A :term:`py:bytes-like object` representing the webhook's default avatar.
            This operates similarly to :meth:`~ClientUser.edit`.
        reason: Optional[:class:`str`]
            The reason for creating this webhook. Shows up in the audit logs.

        Raises
        -------
        HTTPException
            Creating the webhook failed.
        Forbidden
            You do not have permissions to create a webhook.

        Returns
        --------
        :class:`Webhook`
            The created webhook.
        """

        from .webhook import Webhook

        if avatar is not None:
            avatar = utils._bytes_to_base64_data(avatar)  # type: ignore # Silence reassignment error

        data = await self._state.http.create_webhook(self.id, name=str(name), avatar=avatar, reason=reason)
        return Webhook.from_state(data, state=self._state)

    async def archived_threads(
        self,
        *,
        limit: Optional[int] = 100,
        before: Optional[Union[Snowflake, datetime.datetime]] = None,
    ) -> AsyncIterator[Thread]:
        """Returns an :term:`asynchronous iterator` that iterates over all archived threads in this forum
        in order of decreasing :attr:`Thread.archive_timestamp`.

        You must have :attr:`~Permissions.read_message_history` to do this.

        .. versionadded:: 2.0

        Parameters
        -----------
        limit: Optional[:class:`bool`]
            The number of threads to retrieve.
            If ``None``, retrieves every archived thread in the channel. Note, however,
            that this would make it a slow operation.
        before: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]
            Retrieve archived channels before the given date or ID.

        Raises
        ------
        Forbidden
            You do not have permissions to get archived threads.
        HTTPException
            The request to get the archived threads failed.

        Yields
        -------
        :class:`Thread`
            The archived threads.
        """
        before_timestamp = None

        if isinstance(before, datetime.datetime):
            before_timestamp = before.isoformat()
        elif before is not None:
            before_timestamp = utils.snowflake_time(before.id).isoformat()

        update_before = lambda data: data['thread_metadata']['archive_timestamp']

        while True:
            retrieve = 100
            if limit is not None:
                if limit <= 0:
                    return
                retrieve = max(2, min(retrieve, limit))

            data = await self.guild._state.http.get_public_archived_threads(self.id, before=before_timestamp, limit=retrieve)

            threads = data.get('threads', [])
            for raw_thread in threads:
                yield Thread(guild=self.guild, state=self.guild._state, data=raw_thread)
                # Currently the API doesn't let you request less than 2 threads.
                # Bail out early if we had to retrieve more than what the limit was.
                if limit is not None:
                    limit -= 1
                    if limit <= 0:
                        return

            if not data.get('has_more', False):
                return

            before_timestamp = update_before(threads[-1])


class DMChannel(discord.abc.Messageable, discord.abc.PrivateChannel, Hashable):
    """Represents a Discord direct message channel.

    .. container:: operations

        .. describe:: x == y

            Checks if two channels are equal.

        .. describe:: x != y

            Checks if two channels are not equal.

        .. describe:: hash(x)

            Returns the channel's hash.

        .. describe:: str(x)

            Returns a string representation of the channel

    Attributes
    ----------
    recipient: Optional[:class:`User`]
        The user you are participating with in the direct message channel.
        If this channel is received through the gateway, the recipient information
        may not be always available.
    recipients: List[:class:`User`]
        The users you are participating with in the DM channel.

        .. versionadded:: 2.4
    me: :class:`ClientUser`
        The user presenting yourself.
    id: :class:`int`
        The direct message channel ID.
    """

    __slots__ = ('id', 'recipients', 'me', '_state')

    def __init__(self, *, me: ClientUser, state: ConnectionState, data: DMChannelPayload):
        self._state: ConnectionState = state
        self.recipients: List[User] = [state.store_user(u) for u in data.get('recipients', [])]
        self.me: ClientUser = me
        self.id: int = int(data['id'])

    async def _get_channel(self) -> Self:
        return self

    def __str__(self) -> str:
        if self.recipient:
            return f'Direct Message with {self.recipient}'
        return 'Direct Message with Unknown User'

    def __repr__(self) -> str:
        return f'<DMChannel id={self.id} recipient={self.recipient!r}>'

    @classmethod
    def _from_message(cls, state: ConnectionState, channel_id: int) -> Self:
        self = cls.__new__(cls)
        self._state = state
        self.id = channel_id
        self.recipients = []
        # state.user won't be None here
        self.me = state.user  # type: ignore
        return self

    @property
    def recipient(self) -> Optional[User]:
        if self.recipients:
            return self.recipients[0]
        return None

    @property
    def type(self) -> Literal[ChannelType.private]:
        """:class:`ChannelType`: The channel's Discord type."""
        return ChannelType.private

    @property
    def guild(self) -> Optional[Guild]:
        """Optional[:class:`Guild`]: The guild this DM channel belongs to. Always ``None``.

        This is mainly provided for compatibility purposes in duck typing.

        .. versionadded:: 2.0
        """
        return None

    @property
    def jump_url(self) -> str:
        """:class:`str`: Returns a URL that allows the client to jump to the channel.

        .. versionadded:: 2.0
        """
        return f'https://discord.com/channels/@me/{self.id}'

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the direct message channel's creation time in UTC."""
        return utils.snowflake_time(self.id)

    def permissions_for(self, obj: Any = None, /) -> Permissions:
        """Handles permission resolution for a :class:`User`.

        This function is there for compatibility with other channel types.

        Actual direct messages do not really have the concept of permissions.

        This returns all the Text related permissions set to ``True`` except:

        - :attr:`~Permissions.send_tts_messages`: You cannot send TTS messages in a DM.
        - :attr:`~Permissions.manage_messages`: You cannot delete others messages in a DM.
        - :attr:`~Permissions.create_private_threads`: There are no threads in a DM.
        - :attr:`~Permissions.create_public_threads`: There are no threads in a DM.
        - :attr:`~Permissions.manage_threads`: There are no threads in a DM.
        - :attr:`~Permissions.send_messages_in_threads`: There are no threads in a DM.

        .. versionchanged:: 2.0

            ``obj`` parameter is now positional-only.

        .. versionchanged:: 2.1

            Thread related permissions are now set to ``False``.

        Parameters
        -----------
        obj: :class:`User`
            The user to check permissions for. This parameter is ignored
            but kept for compatibility with other ``permissions_for`` methods.

        Returns
        --------
        :class:`Permissions`
            The resolved permissions.
        """
        return Permissions._dm_permissions()

    def get_partial_message(self, message_id: int, /) -> PartialMessage:
        """Creates a :class:`PartialMessage` from the message ID.

        This is useful if you want to work with a message and only have its ID without
        doing an unnecessary API call.

        .. versionadded:: 1.6

        .. versionchanged:: 2.0

            ``message_id`` parameter is now positional-only.

        Parameters
        ------------
        message_id: :class:`int`
            The message ID to create a partial message for.

        Returns
        ---------
        :class:`PartialMessage`
            The partial message.
        """

        from .message import PartialMessage

        return PartialMessage(channel=self, id=message_id)


class GroupChannel(discord.abc.Messageable, discord.abc.PrivateChannel, Hashable):
    """Represents a Discord group channel.

    .. container:: operations

        .. describe:: x == y

            Checks if two channels are equal.

        .. describe:: x != y

            Checks if two channels are not equal.

        .. describe:: hash(x)

            Returns the channel's hash.

        .. describe:: str(x)

            Returns a string representation of the channel

    Attributes
    ----------
    recipients: List[:class:`User`]
        The users you are participating with in the group channel.
    me: :class:`ClientUser`
        The user presenting yourself.
    id: :class:`int`
        The group channel ID.
    owner: Optional[:class:`User`]
        The user that owns the group channel.
    owner_id: :class:`int`
        The owner ID that owns the group channel.

        .. versionadded:: 2.0
    name: Optional[:class:`str`]
        The group channel's name if provided.
    """

    __slots__ = ('id', 'recipients', 'owner_id', 'owner', '_icon', 'name', 'me', '_state')

    def __init__(self, *, me: ClientUser, state: ConnectionState, data: GroupChannelPayload):
        self._state: ConnectionState = state
        self.id: int = int(data['id'])
        self.me: ClientUser = me
        self._update_group(data)

    def _update_group(self, data: GroupChannelPayload) -> None:
        self.owner_id: Optional[int] = utils._get_as_snowflake(data, 'owner_id')
        self._icon: Optional[str] = data.get('icon')
        self.name: Optional[str] = data.get('name')
        self.recipients: List[User] = [self._state.store_user(u) for u in data.get('recipients', [])]

        self.owner: Optional[BaseUser]
        if self.owner_id == self.me.id:
            self.owner = self.me
        else:
            self.owner = utils.find(lambda u: u.id == self.owner_id, self.recipients)

    async def _get_channel(self) -> Self:
        return self

    def __str__(self) -> str:
        if self.name:
            return self.name

        if len(self.recipients) == 0:
            return 'Unnamed'

        return ', '.join(map(lambda x: x.name, self.recipients))

    def __repr__(self) -> str:
        return f'<GroupChannel id={self.id} name={self.name!r}>'

    @property
    def type(self) -> Literal[ChannelType.group]:
        """:class:`ChannelType`: The channel's Discord type."""
        return ChannelType.group

    @property
    def guild(self) -> Optional[Guild]:
        """Optional[:class:`Guild`]: The guild this group channel belongs to. Always ``None``.

        This is mainly provided for compatibility purposes in duck typing.

        .. versionadded:: 2.0
        """
        return None

    @property
    def icon(self) -> Optional[Asset]:
        """Optional[:class:`Asset`]: Returns the channel's icon asset if available."""
        if self._icon is None:
            return None
        return Asset._from_icon(self._state, self.id, self._icon, path='channel')

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the channel's creation time in UTC."""
        return utils.snowflake_time(self.id)

    @property
    def jump_url(self) -> str:
        """:class:`str`: Returns a URL that allows the client to jump to the channel.

        .. versionadded:: 2.0
        """
        return f'https://discord.com/channels/@me/{self.id}'

    def permissions_for(self, obj: Snowflake, /) -> Permissions:
        """Handles permission resolution for a :class:`User`.

        This function is there for compatibility with other channel types.

        Actual direct messages do not really have the concept of permissions.

        This returns all the Text related permissions set to ``True`` except:

        - :attr:`~Permissions.send_tts_messages`: You cannot send TTS messages in a DM.
        - :attr:`~Permissions.manage_messages`: You cannot delete others messages in a DM.
        - :attr:`~Permissions.create_private_threads`: There are no threads in a DM.
        - :attr:`~Permissions.create_public_threads`: There are no threads in a DM.
        - :attr:`~Permissions.manage_threads`: There are no threads in a DM.
        - :attr:`~Permissions.send_messages_in_threads`: There are no threads in a DM.

        This also checks the kick_members permission if the user is the owner.

        .. versionchanged:: 2.0

            ``obj`` parameter is now positional-only.

        .. versionchanged:: 2.1

            Thread related permissions are now set to ``False``.

        Parameters
        -----------
        obj: :class:`~discord.abc.Snowflake`
            The user to check permissions for.

        Returns
        --------
        :class:`Permissions`
            The resolved permissions for the user.
        """

        base = Permissions._dm_permissions()
        base.mention_everyone = True

        if obj.id == self.owner_id:
            base.kick_members = True

        return base

    async def leave(self) -> None:
        """|coro|

        Leave the group.

        If you are the only one in the group, this deletes it as well.

        Raises
        -------
        HTTPException
            Leaving the group failed.
        """

        await self._state.http.leave_group(self.id)


class PartialMessageable(discord.abc.Messageable, Hashable):
    """Represents a partial messageable to aid with working messageable channels when
    only a channel ID is present.

    The only way to construct this class is through :meth:`Client.get_partial_messageable`.

    Note that this class is trimmed down and has no rich attributes.

    .. versionadded:: 2.0

    .. container:: operations

        .. describe:: x == y

            Checks if two partial messageables are equal.

        .. describe:: x != y

            Checks if two partial messageables are not equal.

        .. describe:: hash(x)

            Returns the partial messageable's hash.

    Attributes
    -----------
    id: :class:`int`
        The channel ID associated with this partial messageable.
    guild_id: Optional[:class:`int`]
        The guild ID associated with this partial messageable.
    type: Optional[:class:`ChannelType`]
        The channel type associated with this partial messageable, if given.
    """

    def __init__(self, state: ConnectionState, id: int, guild_id: Optional[int] = None, type: Optional[ChannelType] = None):
        self._state: ConnectionState = state
        self.id: int = id
        self.guild_id: Optional[int] = guild_id
        self.type: Optional[ChannelType] = type

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id} type={self.type!r}>'

    async def _get_channel(self) -> PartialMessageable:
        return self

    @property
    def guild(self) -> Optional[Guild]:
        """Optional[:class:`Guild`]: The guild this partial messageable is in."""
        return self._state._get_guild(self.guild_id)

    @property
    def jump_url(self) -> str:
        """:class:`str`: Returns a URL that allows the client to jump to the channel."""
        if self.guild_id is None:
            return f'https://discord.com/channels/@me/{self.id}'
        return f'https://discord.com/channels/{self.guild_id}/{self.id}'

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the channel's creation time in UTC."""
        return utils.snowflake_time(self.id)

    def permissions_for(self, obj: Any = None, /) -> Permissions:
        """Handles permission resolution for a :class:`User`.

        This function is there for compatibility with other channel types.

        Since partial messageables cannot reasonably have the concept of
        permissions, this will always return :meth:`Permissions.none`.

        Parameters
        -----------
        obj: :class:`User`
            The user to check permissions for. This parameter is ignored
            but kept for compatibility with other ``permissions_for`` methods.

        Returns
        --------
        :class:`Permissions`
            The resolved permissions.
        """

        return Permissions.none()

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string that allows you to mention the channel.

        .. versionadded:: 2.5
        """
        return f'<#{self.id}>'

    def get_partial_message(self, message_id: int, /) -> PartialMessage:
        """Creates a :class:`PartialMessage` from the message ID.

        This is useful if you want to work with a message and only have its ID without
        doing an unnecessary API call.

        Parameters
        ------------
        message_id: :class:`int`
            The message ID to create a partial message for.

        Returns
        ---------
        :class:`PartialMessage`
            The partial message.
        """

        from .message import PartialMessage

        return PartialMessage(channel=self, id=message_id)

