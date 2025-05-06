from __future__ import annotations

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    NamedTuple,
    Optional,
    TYPE_CHECKING,
    Tuple,
    TypeVar,
    Union,
    overload,
)
import datetime

from .... import abc
from ..scheduled_event import ScheduledEvent
from ....utils.permissions import PermissionOverwrite, Permissions
from ..enums import PrivacyLevel
from .enums import ChannelType, VideoQualityMode, VoiceChannelEffectAnimationType
from ...components.enums import EntityType

from ....utils.mixins import Hashable
from ....utils import utils
from ....utils.utils import MISSING
from ....errors import ClientException
from .stage_instance import StageInstance
from ...emoji.partial import PartialEmoji
from ....utils.object import Object
from ..soundboard import BaseSoundboardSound, SoundboardDefaultSound

from ....utils.enums import try_enum 
from .other import CategoryChannel

__all__ = (
    'VoiceChannel',
    'StageChannel',
    'VoiceChannelEffect',
    'VoiceChannelSoundEffect',
    'VocalGuildChannel'
    
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..role import Role
    from ..member import Member, VoiceState
    from ....abc import Snowflake, SnowflakeTime
    from ...message.messages import Message, PartialMessage
    from ...webhook import Webhook
    from ...state import ConnectionState
    from ...user.user import BaseUser
    from ..guilds import Guild

    from .types import VoiceChannelPayload, StageChannelPayload, VoiceChannelEffectPayload
    from ....utils.snowflake import SnowflakeList
    from ..soundboard.types import BaseSoundboardSoundPayload
    from ..soundboard import SoundboardSound

    OverwriteKeyT = TypeVar('OverwriteKeyT', Role, BaseUser, Object, Union[Role, Member, Object])







class VoiceChannelEffectAnimation(NamedTuple):
    id: int
    type: VoiceChannelEffectAnimationType


class VoiceChannelSoundEffect(BaseSoundboardSound):

    __slots__ = ('_state',)

    def __init__(self, *, state: ConnectionState, id: int, volume: float):
        data: BaseSoundboardSoundPayload = {
            'sound_id': id,
            'volume': volume,
        }
        super().__init__(state=state, data=data)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} volume={self.volume}>"

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        """Optional[:class:`datetime.datetime`]: Returns the snowflake's creation time in UTC.
        Returns ``None`` if it's a default sound."""
        if self.is_default():
            return None
        else:
            return utils.snowflake_time(self.id)

    def is_default(self) -> bool:
        """:class:`bool`: Whether it's a default sound or not."""
        # if it's smaller than the Discord Epoch it cannot be a snowflake
        return self.id < utils.DISCORD_EPOCH


class VoiceChannelEffect:

    __slots__ = ('channel', 'user', 'animation', 'emoji', 'sound')

    def __init__(self, *, state: ConnectionState, data: VoiceChannelEffectPayload, guild: Guild):
        self.channel: VoiceChannel = guild.get_channel(int(data['channel_id']))  # type: ignore # will always be a VoiceChannel
        self.user: Optional[Member] = guild.get_member(int(data['user_id']))
        self.animation: Optional[VoiceChannelEffectAnimation] = None

        animation_id = data.get('animation_id')
        if animation_id is not None:
            animation_type = try_enum(VoiceChannelEffectAnimationType, data['animation_type'])  # type: ignore # cannot be None here
            self.animation = VoiceChannelEffectAnimation(id=animation_id, type=animation_type)

        emoji = data.get('emoji')
        self.emoji: Optional[PartialEmoji] = PartialEmoji.from_dict(emoji) if emoji is not None else None
        self.sound: Optional[VoiceChannelSoundEffect] = None

        sound_id: Optional[int] = utils._get_as_snowflake(data, 'sound_id')
        if sound_id is not None:
            sound_volume = data.get('sound_volume') or 0.0
            self.sound = VoiceChannelSoundEffect(state=state, id=sound_id, volume=sound_volume)

    def __repr__(self) -> str:
        attrs = [
            ('channel', self.channel),
            ('user', self.user),
            ('animation', self.animation),
            ('emoji', self.emoji),
            ('sound', self.sound),
        ]
        inner = ' '.join('%s=%r' % t for t in attrs)
        return f"<{self.__class__.__name__} {inner}>"

    def is_sound(self) -> bool:
        """:class:`bool`: Whether the effect is a sound or not."""
        return self.sound is not None




class VocalGuildChannel(abc.Messageable, abc.Connectable, abc.GuildChannel, Hashable):
    __slots__ = (
        'name',
        'id',
        'guild',
        'nsfw',
        'bitrate',
        'user_limit',
        '_state',
        'position',
        'slowmode_delay',
        '_overwrites',
        'category_id',
        'rtc_region',
        'video_quality_mode',
        'last_message_id',
    )

    def __init__(self, *, state: ConnectionState, guild: Guild, data: Union[VoiceChannelPayload, StageChannelPayload]):
        self._state: ConnectionState = state
        self.id: int = int(data['id'])
        self._update(guild, data)

    async def _get_channel(self) -> Self:
        return self

    def _get_voice_client_key(self) -> Tuple[int, str]:
        return self.guild.id, 'guild_id'

    def _get_voice_state_pair(self) -> Tuple[int, int]:
        return self.guild.id, self.id

    def _update(self, guild: Guild, data: Union[VoiceChannelPayload, StageChannelPayload]) -> None:
        self.guild: Guild = guild
        self.name: str = data['name']
        self.nsfw: bool = data.get('nsfw', False)
        self.rtc_region: Optional[str] = data.get('rtc_region')
        self.video_quality_mode: VideoQualityMode = try_enum(VideoQualityMode, data.get('video_quality_mode', 1))
        self.category_id: Optional[int] = utils._get_as_snowflake(data, 'parent_id')
        self.last_message_id: Optional[int] = utils._get_as_snowflake(data, 'last_message_id')
        self.position: int = data['position']
        self.slowmode_delay = data.get('rate_limit_per_user', 0)
        self.bitrate: int = data['bitrate']
        self.user_limit: int = data['user_limit']
        self._fill_overwrites(data)

    @property
    def _sorting_bucket(self) -> int:
        return ChannelType.voice.value

    def is_nsfw(self) -> bool:
        """:class:`bool`: Checks if the channel is NSFW.

        .. versionadded:: 2.0
        """
        return self.nsfw

    @property
    def members(self) -> List[Member]:
        """List[:class:`Member`]: Returns all members that are currently inside this voice channel."""
        ret = []
        for user_id, state in self.guild._voice_states.items():
            if state.channel and state.channel.id == self.id:
                member = self.guild.get_member(user_id)
                if member is not None:
                    ret.append(member)
        return ret

    @property
    def voice_states(self) -> Dict[int, VoiceState]:
        """Returns a mapping of member IDs who have voice states in this channel.

        .. versionadded:: 1.3

        .. note::

            This function is intentionally low level to replace :attr:`members`
            when the member cache is unavailable.

        Returns
        --------
        Mapping[:class:`int`, :class:`VoiceState`]
            The mapping of member ID to a voice state.
        """
        # fmt: off
        return {
            key: value
            for key, value in self.guild._voice_states.items()
            if value.channel and value.channel.id == self.id
        }
        # fmt: on

    @property
    def scheduled_events(self) -> List[ScheduledEvent]:
        """List[:class:`ScheduledEvent`]: Returns all scheduled events for this channel.

        .. versionadded:: 2.0
        """
        return [event for event in self.guild.scheduled_events if event.channel_id == self.id]

    @utils.copy_doc(abc.GuildChannel.permissions_for)
    def permissions_for(self, obj: Union[Member, Role], /) -> Permissions:
        base = super().permissions_for(obj)
        self._apply_implicit_permissions(base)

        # voice channels cannot be edited by people who can't connect to them
        # It also implicitly denies all other voice perms
        if not base.connect:
            denied = Permissions.voice()
            denied.update(manage_channels=True, manage_roles=True)
            base.value &= ~denied.value
        return base

    @property
    def last_message(self) -> Optional[Message]:
        """Retrieves the last message from this channel in cache.

        The message might not be valid or point to an existing message.

        .. versionadded:: 2.0

        .. admonition:: Reliable Fetching
            :class: helpful

            For a slightly more reliable method of fetching the
            last message, consider using either :meth:`history`
            or :meth:`fetch_message` with the :attr:`last_message_id`
            attribute.

        Returns
        ---------
        Optional[:class:`Message`]
            The last message in this channel or ``None`` if not found.
        """
        return self._state._get_message(self.last_message_id) if self.last_message_id else None

    def get_partial_message(self, message_id: int, /) -> PartialMessage:
        """Creates a :class:`PartialMessage` from the message ID.

        This is useful if you want to work with a message and only have its ID without
        doing an unnecessary API call.

        .. versionadded:: 2.0

        Parameters
        ------------
        message_id: :class:`int`
            The message ID to create a partial message for.

        Returns
        ---------
        :class:`PartialMessage`
            The partial message.
        """

        from ...message import PartialMessage

        return PartialMessage(channel=self, id=message_id)  # type: ignore # VocalGuildChannel is an impl detail

    async def delete_messages(self, messages: Iterable[Snowflake], *, reason: Optional[str] = None) -> None:
        """|coro|

        Deletes a list of messages. This is similar to :meth:`Message.delete`
        except it bulk deletes multiple messages.

        As a special case, if the number of messages is 0, then nothing
        is done. If the number of messages is 1 then single message
        delete is done. If it's more than two, then bulk delete is used.

        You cannot bulk delete more than 100 messages or messages that
        are older than 14 days old.

        You must have :attr:`~Permissions.manage_messages` to do this.

        .. versionadded:: 2.0

        Parameters
        -----------
        messages: Iterable[:class:`abc.Snowflake`]
            An iterable of messages denoting which ones to bulk delete.
        reason: Optional[:class:`str`]
            The reason for deleting the messages. Shows up on the audit log.

        Raises
        ------
        ClientException
            The number of messages to delete was more than 100.
        Forbidden
            You do not have proper permissions to delete the messages.
        NotFound
            If single delete, then the message was already deleted.
        HTTPException
            Deleting the messages failed.
        """
        if not isinstance(messages, (list, tuple)):
            messages = list(messages)

        if len(messages) == 0:
            return  # do nothing

        if len(messages) == 1:
            message_id: int = messages[0].id
            await self._state.http.delete_message(self.id, message_id)
            return

        if len(messages) > 100:
            raise ClientException('Can only bulk delete messages up to 100 messages')

        message_ids: SnowflakeList = [m.id for m in messages]
        await self._state.http.delete_messages(self.id, message_ids, reason=reason)

    async def purge(
        self,
        *,
        limit: Optional[int] = 100,
        check: Callable[[Message], bool] = MISSING,
        before: Optional[SnowflakeTime] = None,
        after: Optional[SnowflakeTime] = None,
        around: Optional[SnowflakeTime] = None,
        oldest_first: Optional[bool] = None,
        bulk: bool = True,
        reason: Optional[str] = None,
    ) -> List[Message]:
        """|coro|

        Purges a list of messages that meet the criteria given by the predicate
        ``check``. If a ``check`` is not provided then all messages are deleted
        without discrimination.

        You must have :attr:`~Permissions.manage_messages` to
        delete messages even if they are your own.
        Having :attr:`~Permissions.read_message_history` is
        also needed to retrieve message history.

        .. versionadded:: 2.0

        Examples
        ---------

        Deleting bot's messages ::

            def is_me(m):
                return m.author == client.user

            deleted = await channel.purge(limit=100, check=is_me)
            await channel.send(f'Deleted {len(deleted)} message(s)')

        Parameters
        -----------
        limit: Optional[:class:`int`]
            The number of messages to search through. This is not the number
            of messages that will be deleted, though it can be.
        check: Callable[[:class:`Message`], :class:`bool`]
            The function used to check if a message should be deleted.
            It must take a :class:`Message` as its sole parameter.
        before: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]
            Same as ``before`` in :meth:`history`.
        after: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]
            Same as ``after`` in :meth:`history`.
        around: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]
            Same as ``around`` in :meth:`history`.
        oldest_first: Optional[:class:`bool`]
            Same as ``oldest_first`` in :meth:`history`.
        bulk: :class:`bool`
            If ``True``, use bulk delete. Setting this to ``False`` is useful for mass-deleting
            a bot's own messages without :attr:`Permissions.manage_messages`. When ``True``, will
            fall back to single delete if messages are older than two weeks.
        reason: Optional[:class:`str`]
            The reason for purging the messages. Shows up on the audit log.

        Raises
        -------
        Forbidden
            You do not have proper permissions to do the actions required.
        HTTPException
            Purging the messages failed.

        Returns
        --------
        List[:class:`.Message`]
            The list of messages that were deleted.
        """

        return await abc._purge_helper(
            self,
            limit=limit,
            check=check,
            before=before,
            after=after,
            around=around,
            oldest_first=oldest_first,
            bulk=bulk,
            reason=reason,
        )

    async def webhooks(self) -> List[Webhook]:
        """|coro|

        Gets the list of webhooks from this channel.

        You must have :attr:`~.Permissions.manage_webhooks` to do this.

        .. versionadded:: 2.0

        Raises
        -------
        Forbidden
            You don't have permissions to get the webhooks.

        Returns
        --------
        List[:class:`Webhook`]
            The webhooks for this channel.
        """

        from ...webhook import Webhook

        data = await self._state.http.channel_webhooks(self.id)
        return [Webhook.from_state(d, state=self._state) for d in data]

    async def create_webhook(self, *, name: str, avatar: Optional[bytes] = None, reason: Optional[str] = None) -> Webhook:
        """|coro|

        Creates a webhook for this channel.

        You must have :attr:`~.Permissions.manage_webhooks` to do this.

        .. versionadded:: 2.0

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

        from ...webhook import Webhook

        if avatar is not None:
            avatar = utils._bytes_to_base64_data(avatar)  # type: ignore # Silence reassignment error

        data = await self._state.http.create_webhook(self.id, name=str(name), avatar=avatar, reason=reason)
        return Webhook.from_state(data, state=self._state)

    @utils.copy_doc(abc.GuildChannel.clone)
    async def clone(
        self, *, name: Optional[str] = None, category: Optional[CategoryChannel] = None, reason: Optional[str] = None
    ) -> Self:
        base = {
            'bitrate': self.bitrate,
            'user_limit': self.user_limit,
            'rate_limit_per_user': self.slowmode_delay,
            'nsfw': self.nsfw,
            'video_quality_mode': self.video_quality_mode.value,
        }
        if self.rtc_region:
            base['rtc_region'] = self.rtc_region

        return await self._clone_impl(
            base,
            name=name,
            category=category,
            reason=reason,
        )


class VoiceChannel(VocalGuildChannel):
    """Represents a Discord guild voice channel.

    .. container:: operations

        .. describe:: x == y

            Checks if two channels are equal.

        .. describe:: x != y

            Checks if two channels are not equal.

        .. describe:: hash(x)

            Returns the channel's hash.

        .. describe:: str(x)

            Returns the channel's name.

    Attributes
    -----------
    name: :class:`str`
        The channel name.
    guild: :class:`Guild`
        The guild the channel belongs to.
    id: :class:`int`
        The channel ID.
    nsfw: :class:`bool`
        If the channel is marked as "not safe for work" or "age restricted".

        .. versionadded:: 2.0
    category_id: Optional[:class:`int`]
        The category channel ID this channel belongs to, if applicable.
    position: :class:`int`
        The position in the channel list. This is a number that starts at 0. e.g. the
        top channel is position 0.
    bitrate: :class:`int`
        The channel's preferred audio bitrate in bits per second.
    user_limit: :class:`int`
        The channel's limit for number of members that can be in a voice channel.
    rtc_region: Optional[:class:`str`]
        The region for the voice channel's voice communication.
        A value of ``None`` indicates automatic voice region detection.

        .. versionadded:: 1.7

        .. versionchanged:: 2.0
            The type of this attribute has changed to :class:`str`.
    video_quality_mode: :class:`VideoQualityMode`
        The camera video quality for the voice channel's participants.

        .. versionadded:: 2.0
    last_message_id: Optional[:class:`int`]
        The last message ID of the message sent to this channel. It may
        *not* point to an existing or valid message.

        .. versionadded:: 2.0
    slowmode_delay: :class:`int`
        The number of seconds a member must wait between sending messages
        in this channel. A value of ``0`` denotes that it is disabled.
        Bots and users with :attr:`~Permissions.manage_channels` or
        :attr:`~Permissions.manage_messages` bypass slowmode.

        .. versionadded:: 2.2
    """

    __slots__ = ()

    def __repr__(self) -> str:
        attrs = [
            ('id', self.id),
            ('name', self.name),
            ('rtc_region', self.rtc_region),
            ('position', self.position),
            ('bitrate', self.bitrate),
            ('video_quality_mode', self.video_quality_mode),
            ('user_limit', self.user_limit),
            ('category_id', self.category_id),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    @property
    def _scheduled_event_entity_type(self) -> Optional[EntityType]:
        return EntityType.voice

    @property
    def type(self) -> Literal[ChannelType.voice]:
        """:class:`ChannelType`: The channel's Discord type."""
        return ChannelType.voice

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
        nsfw: bool = ...,
        bitrate: int = ...,
        user_limit: int = ...,
        position: int = ...,
        sync_permissions: int = ...,
        category: Optional[CategoryChannel] = ...,
        overwrites: Mapping[OverwriteKeyT, PermissionOverwrite] = ...,
        rtc_region: Optional[str] = ...,
        video_quality_mode: VideoQualityMode = ...,
        slowmode_delay: int = ...,
        status: Optional[str] = ...,
        reason: Optional[str] = ...,
    ) -> VoiceChannel:
        ...

    async def edit(self, *, reason: Optional[str] = None, **options: Any) -> Optional[VoiceChannel]:
        """|coro|

        Edits the channel.

        You must have :attr:`~Permissions.manage_channels` to do this.

        .. versionchanged:: 1.3
            The ``overwrites`` keyword-only parameter was added.

        .. versionchanged:: 2.0
            Edits are no longer in-place, the newly edited channel is returned instead.

        .. versionchanged:: 2.0
            The ``region`` parameter now accepts :class:`str` instead of an enum.

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` instead of
            ``InvalidArgument``.

        Parameters
        ----------
        name: :class:`str`
            The new channel's name.
        bitrate: :class:`int`
            The new channel's bitrate.
        nsfw: :class:`bool`
            To mark the channel as NSFW or not.
        user_limit: :class:`int`
            The new channel's user limit.
        position: :class:`int`
            The new channel's position.
        sync_permissions: :class:`bool`
            Whether to sync permissions with the channel's new or pre-existing
            category. Defaults to ``False``.
        category: Optional[:class:`CategoryChannel`]
            The new category for this channel. Can be ``None`` to remove the
            category.
        slowmode_delay: :class:`int`
            Specifies the slowmode rate limit for user in this channel, in seconds.
            A value of ``0`` disables slowmode. The maximum value possible is ``21600``.
        reason: Optional[:class:`str`]
            The reason for editing this channel. Shows up on the audit log.
        overwrites: :class:`Mapping`
            A :class:`Mapping` of target (either a role or a member) to
            :class:`PermissionOverwrite` to apply to the channel.
        rtc_region: Optional[:class:`str`]
            The new region for the voice channel's voice communication.
            A value of ``None`` indicates automatic voice region detection.

            .. versionadded:: 1.7
        video_quality_mode: :class:`VideoQualityMode`
            The camera video quality for the voice channel's participants.

            .. versionadded:: 2.0
        status: Optional[:class:`str`]
            The new voice channel status. It can be up to 500 characters.
            Can be ``None`` to remove the status.

            .. versionadded:: 2.4

        Raises
        ------
        TypeError
            If the permission overwrite information is not in proper form.
        Forbidden
            You do not have permissions to edit the channel.
        HTTPException
            Editing the channel failed.

        Returns
        --------
        Optional[:class:`.VoiceChannel`]
            The newly edited voice channel. If the edit was only positional
            then ``None`` is returned instead.
        """
        payload = await self._edit(options, reason=reason)
        if payload is not None:
            # the payload will always be the proper channel payload
            return self.__class__(state=self._state, guild=self.guild, data=payload)  # type: ignore

    async def send_sound(self, sound: Union[SoundboardSound, SoundboardDefaultSound], /) -> None:
        """|coro|

        Sends a soundboard sound for this channel.

        You must have :attr:`~Permissions.speak` and :attr:`~Permissions.use_soundboard` to do this.
        Additionally, you must have :attr:`~Permissions.use_external_sounds` if the sound is from
        a different guild.

        .. versionadded:: 2.5

        Parameters
        -----------
        sound: Union[:class:`SoundboardSound`, :class:`SoundboardDefaultSound`]
            The sound to send for this channel.

        Raises
        -------
        Forbidden
            You do not have permissions to send a sound for this channel.
        HTTPException
            Sending the sound failed.
        """
        payload = {'sound_id': sound.id}
        if not isinstance(sound, SoundboardDefaultSound) and self.guild.id != sound.guild.id:
            payload['source_guild_id'] = sound.guild.id

        await self._state.http.send_soundboard_sound(self.id, **payload)


class StageChannel(VocalGuildChannel):
    """Represents a Discord guild stage channel.

    .. versionadded:: 1.7

    .. container:: operations

        .. describe:: x == y

            Checks if two channels are equal.

        .. describe:: x != y

            Checks if two channels are not equal.

        .. describe:: hash(x)

            Returns the channel's hash.

        .. describe:: str(x)

            Returns the channel's name.

    Attributes
    -----------
    name: :class:`str`
        The channel name.
    guild: :class:`Guild`
        The guild the channel belongs to.
    id: :class:`int`
        The channel ID.
    nsfw: :class:`bool`
        If the channel is marked as "not safe for work" or "age restricted".

        .. versionadded:: 2.0
    topic: Optional[:class:`str`]
        The channel's topic. ``None`` if it isn't set.
    category_id: Optional[:class:`int`]
        The category channel ID this channel belongs to, if applicable.
    position: :class:`int`
        The position in the channel list. This is a number that starts at 0. e.g. the
        top channel is position 0.
    bitrate: :class:`int`
        The channel's preferred audio bitrate in bits per second.
    user_limit: :class:`int`
        The channel's limit for number of members that can be in a stage channel.
    rtc_region: Optional[:class:`str`]
        The region for the stage channel's voice communication.
        A value of ``None`` indicates automatic voice region detection.
    video_quality_mode: :class:`VideoQualityMode`
        The camera video quality for the stage channel's participants.

        .. versionadded:: 2.0
    last_message_id: Optional[:class:`int`]
        The last message ID of the message sent to this channel. It may
        *not* point to an existing or valid message.

        .. versionadded:: 2.2
    slowmode_delay: :class:`int`
        The number of seconds a member must wait between sending messages
        in this channel. A value of ``0`` denotes that it is disabled.
        Bots and users with :attr:`~Permissions.manage_channels` or
        :attr:`~Permissions.manage_messages` bypass slowmode.

        .. versionadded:: 2.2
    """

    __slots__ = ('topic',)

    def __repr__(self) -> str:
        attrs = [
            ('id', self.id),
            ('name', self.name),
            ('topic', self.topic),
            ('rtc_region', self.rtc_region),
            ('position', self.position),
            ('bitrate', self.bitrate),
            ('video_quality_mode', self.video_quality_mode),
            ('user_limit', self.user_limit),
            ('category_id', self.category_id),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    def _update(self, guild: Guild, data: StageChannelPayload) -> None:
        super()._update(guild, data)
        self.topic: Optional[str] = data.get('topic')

    @property
    def _scheduled_event_entity_type(self) -> Optional[EntityType]:
        return EntityType.stage_instance

    @property
    def requesting_to_speak(self) -> List[Member]:
        """List[:class:`Member`]: A list of members who are requesting to speak in the stage channel."""
        return [member for member in self.members if member.voice and member.voice.requested_to_speak_at is not None]

    @property
    def speakers(self) -> List[Member]:
        """List[:class:`Member`]: A list of members who have been permitted to speak in the stage channel.

        .. versionadded:: 2.0
        """
        return [
            member
            for member in self.members
            if member.voice and not member.voice.suppress and member.voice.requested_to_speak_at is None
        ]

    @property
    def listeners(self) -> List[Member]:
        """List[:class:`Member`]: A list of members who are listening in the stage channel.

        .. versionadded:: 2.0
        """
        return [member for member in self.members if member.voice and member.voice.suppress]

    @property
    def moderators(self) -> List[Member]:
        """List[:class:`Member`]: A list of members who are moderating the stage channel.

        .. versionadded:: 2.0
        """
        required_permissions = Permissions.stage_moderator()
        return [member for member in self.members if self.permissions_for(member) >= required_permissions]

    @property
    def type(self) -> Literal[ChannelType.stage_voice]:
        """:class:`ChannelType`: The channel's Discord type."""
        return ChannelType.stage_voice

    @property
    def instance(self) -> Optional[StageInstance]:
        """Optional[:class:`StageInstance`]: The running stage instance of the stage channel.

        .. versionadded:: 2.0
        """
        return utils.get(self.guild.stage_instances, channel_id=self.id)

    async def create_instance(
        self,
        *,
        topic: str,
        privacy_level: PrivacyLevel = MISSING,
        send_start_notification: bool = False,
        scheduled_event: Snowflake = MISSING,
        reason: Optional[str] = None,
    ) -> StageInstance:


        payload: Dict[str, Any] = {'channel_id': self.id, 'topic': topic}

        if privacy_level is not MISSING:
            if not isinstance(privacy_level, PrivacyLevel):
                raise TypeError('privacy_level field must be of type PrivacyLevel')

            payload['privacy_level'] = privacy_level.value

        if scheduled_event is not MISSING:
            payload['guild_scheduled_event_id'] = scheduled_event.id

        payload['send_start_notification'] = send_start_notification

        data = await self._state.http.create_stage_instance(**payload, reason=reason)
        return StageInstance(guild=self.guild, state=self._state, data=data)

    async def fetch_instance(self) -> StageInstance:
        data = await self._state.http.get_stage_instance(self.id)
        return StageInstance(guild=self.guild, state=self._state, data=data)

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
        nsfw: bool = ...,
        bitrate: int = ...,
        user_limit: int = ...,
        position: int = ...,
        sync_permissions: int = ...,
        category: Optional[CategoryChannel] = ...,
        overwrites: Mapping[OverwriteKeyT, PermissionOverwrite] = ...,
        rtc_region: Optional[str] = ...,
        video_quality_mode: VideoQualityMode = ...,
        slowmode_delay: int = ...,
        reason: Optional[str] = ...,
    ) -> StageChannel:
        ...

    async def edit(self, *, reason: Optional[str] = None, **options: Any) -> Optional[StageChannel]:
        """|coro|

        Edits the channel.

        You must have :attr:`~Permissions.manage_channels` to do this.

        .. versionchanged:: 2.0
            The ``topic`` parameter must now be set via :attr:`create_instance`.

        .. versionchanged:: 2.0
            Edits are no longer in-place, the newly edited channel is returned instead.

        .. versionchanged:: 2.0
            The ``region`` parameter now accepts :class:`str` instead of an enum.

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` instead of
            ``InvalidArgument``.

        Parameters
        ----------
        name: :class:`str`
            The new channel's name.
        bitrate: :class:`int`
            The new channel's bitrate.
        position: :class:`int`
            The new channel's position.
        nsfw: :class:`bool`
            To mark the channel as NSFW or not.
        user_limit: :class:`int`
            The new channel's user limit.
        sync_permissions: :class:`bool`
            Whether to sync permissions with the channel's new or pre-existing
            category. Defaults to ``False``.
        category: Optional[:class:`CategoryChannel`]
            The new category for this channel. Can be ``None`` to remove the
            category.
        slowmode_delay: :class:`int`
            Specifies the slowmode rate limit for user in this channel, in seconds.
            A value of ``0`` disables slowmode. The maximum value possible is ``21600``.
        reason: Optional[:class:`str`]
            The reason for editing this channel. Shows up on the audit log.
        overwrites: :class:`Mapping`
            A :class:`Mapping` of target (either a role or a member) to
            :class:`PermissionOverwrite` to apply to the channel.
        rtc_region: Optional[:class:`str`]
            The new region for the stage channel's voice communication.
            A value of ``None`` indicates automatic voice region detection.
        video_quality_mode: :class:`VideoQualityMode`
            The camera video quality for the stage channel's participants.

            .. versionadded:: 2.0

        Raises
        ------
        ValueError
            If the permission overwrite information is not in proper form.
        Forbidden
            You do not have permissions to edit the channel.
        HTTPException
            Editing the channel failed.

        Returns
        --------
        Optional[:class:`.StageChannel`]
            The newly edited stage channel. If the edit was only positional
            then ``None`` is returned instead.
        """

        payload = await self._edit(options, reason=reason)
        if payload is not None:
            # the payload will always be the proper channel payload
            return self.__class__(state=self._state, guild=self.guild, data=payload)  # type: ignore
