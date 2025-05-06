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
    Optional,
    TYPE_CHECKING,
    TypeVar,
    Union,
    overload,
)
import datetime

from .... import abc
from ....utils.permissions import PermissionOverwrite, Permissions
from .enums import ChannelType

from ...components.enums import EntityType
from ....utils.mixins import Hashable
from ....utils import utils
from ....utils.utils import MISSING
from ....errors import ClientException
from ..threads import Thread
from ....utils.object import Object

__all__ = (
    'TextChannel',

)

from .other import CategoryChannel

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..threads.types import ThreadArchiveDuration
    from ..role import Role
    from ..member import Member
    from ....abc import Snowflake, SnowflakeTime
    from ...message.messages import Message, PartialMessage
    from ...webhook import Webhook
    from ...state import ConnectionState
    from ...user.user import BaseUser
    from ..guilds import Guild

    from .types import TextChannelPayload, NewsChannelPayload

    from ....utils.snowflake import SnowflakeList

    OverwriteKeyT = TypeVar('OverwriteKeyT', Role, BaseUser, Object, Union[Role, Member, Object])





class TextChannel(abc.Messageable, abc.GuildChannel, Hashable):
    """Represents a Discord guild text channel.

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
    category_id: Optional[:class:`int`]
        The category channel ID this channel belongs to, if applicable.
    topic: Optional[:class:`str`]
        The channel's topic. ``None`` if it doesn't exist.
    position: :class:`int`
        The position in the channel list. This is a number that starts at 0. e.g. the
        top channel is position 0.
    last_message_id: Optional[:class:`int`]
        The last message ID of the message sent to this channel. It may
        *not* point to an existing or valid message.
    slowmode_delay: :class:`int`
        The number of seconds a member must wait between sending messages
        in this channel. A value of ``0`` denotes that it is disabled.
        Bots and users with :attr:`~Permissions.manage_channels` or
        :attr:`~Permissions.manage_messages` bypass slowmode.
    nsfw: :class:`bool`
        If the channel is marked as "not safe for work" or "age restricted".
    default_auto_archive_duration: :class:`int`
        The default auto archive duration in minutes for threads created in this channel.

        .. versionadded:: 2.0
    default_thread_slowmode_delay: :class:`int`
        The default slowmode delay in seconds for threads created in this channel.

        .. versionadded:: 2.3
    """

    __slots__ = (
        'name',
        'id',
        'guild',
        'topic',
        '_state',
        'nsfw',
        'category_id',
        'position',
        'slowmode_delay',
        '_overwrites',
        '_type',
        'last_message_id',
        'default_auto_archive_duration',
        'default_thread_slowmode_delay',
    )

    def __init__(self, *, state: ConnectionState, guild: Guild, data: Union[TextChannelPayload, NewsChannelPayload]):
        self._state: ConnectionState = state
        self.id: int = int(data['id'])
        self._type: Literal[0, 5] = data['type']
        self._update(guild, data)

    def __repr__(self) -> str:
        attrs = [
            ('id', self.id),
            ('name', self.name),
            ('position', self.position),
            ('nsfw', self.nsfw),
            ('news', self.is_news()),
            ('category_id', self.category_id),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    def _update(self, guild: Guild, data: Union[TextChannelPayload, NewsChannelPayload]) -> None:
        self.guild: Guild = guild
        self.name: str = data['name']
        self.category_id: Optional[int] = utils._get_as_snowflake(data, 'parent_id')
        self.topic: Optional[str] = data.get('topic')
        self.position: int = data['position']
        self.nsfw: bool = data.get('nsfw', False)
        # Does this need coercion into `int`? No idea yet.
        self.slowmode_delay: int = data.get('rate_limit_per_user', 0)
        self.default_auto_archive_duration: ThreadArchiveDuration = data.get('default_auto_archive_duration', 1440)
        self.default_thread_slowmode_delay: int = data.get('default_thread_rate_limit_per_user', 0)
        self._type: Literal[0, 5] = data.get('type', self._type)
        self.last_message_id: Optional[int] = utils._get_as_snowflake(data, 'last_message_id')
        self._fill_overwrites(data)

    async def _get_channel(self) -> Self:
        return self

    @property
    def type(self) -> Literal[ChannelType.text, ChannelType.news]:
        """:class:`ChannelType`: The channel's Discord type."""
        if self._type == 0:
            return ChannelType.text
        return ChannelType.news

    @property
    def _sorting_bucket(self) -> int:
        return ChannelType.text.value

    @property
    def _scheduled_event_entity_type(self) -> Optional[EntityType]:
        return None

    @utils.copy_doc(abc.GuildChannel.permissions_for)
    def permissions_for(self, obj: Union[Member, Role], /) -> Permissions:
        base = super().permissions_for(obj)
        self._apply_implicit_permissions(base)

        # text channels do not have voice related permissions
        denied = Permissions.voice()
        base.value &= ~denied.value
        return base

    @property
    def members(self) -> List[Member]:
        """List[:class:`Member`]: Returns all members that can see this channel."""
        return [m for m in self.guild.members if self.permissions_for(m).read_messages]

    @property
    def threads(self) -> List[Thread]:
        """List[:class:`Thread`]: Returns all the threads that you can see.

        .. versionadded:: 2.0
        """
        return [thread for thread in self.guild._threads.values() if thread.parent_id == self.id]

    def is_nsfw(self) -> bool:
        """:class:`bool`: Checks if the channel is NSFW."""
        return self.nsfw

    def is_news(self) -> bool:
        """:class:`bool`: Checks if the channel is a news channel."""
        return self._type == ChannelType.news.value

    @property
    def last_message(self) -> Optional[Message]:
        """Retrieves the last message from this channel in cache.

        The message might not be valid or point to an existing message.

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

    @overload
    async def edit(self) -> Optional[TextChannel]:
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
        default_thread_slowmode_delay: int = ...,
        type: ChannelType = ...,
        overwrites: Mapping[OverwriteKeyT, PermissionOverwrite] = ...,
    ) -> TextChannel:
        ...

    async def edit(self, *, reason: Optional[str] = None, **options: Any) -> Optional[TextChannel]:
        """|coro|

        Edits the channel.

        You must have :attr:`~Permissions.manage_channels` to do this.

        .. versionchanged:: 1.3
            The ``overwrites`` keyword-only parameter was added.

        .. versionchanged:: 1.4
            The ``type`` keyword-only parameter was added.

        .. versionchanged:: 2.0
            Edits are no longer in-place, the newly edited channel is returned instead.

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` or
            :exc:`ValueError` instead of ``InvalidArgument``.

        Parameters
        ----------
        name: :class:`str`
            The new channel name.
        topic: :class:`str`
            The new channel's topic.
        position: :class:`int`
            The new channel's position.
        nsfw: :class:`bool`
            To mark the channel as NSFW or not.
        sync_permissions: :class:`bool`
            Whether to sync permissions with the channel's new or pre-existing
            category. Defaults to ``False``.
        category: Optional[:class:`CategoryChannel`]
            The new category for this channel. Can be ``None`` to remove the
            category.
        slowmode_delay: :class:`int`
            Specifies the slowmode rate limit for user in this channel, in seconds.
            A value of ``0`` disables slowmode. The maximum value possible is ``21600``.
        type: :class:`ChannelType`
            Change the type of this text channel. Currently, only conversion between
            :attr:`ChannelType.text` and :attr:`ChannelType.news` is supported. This
            is only available to guilds that contain ``NEWS`` in :attr:`Guild.features`.
        reason: Optional[:class:`str`]
            The reason for editing this channel. Shows up on the audit log.
        overwrites: :class:`Mapping`
            A :class:`Mapping` of target (either a role or a member) to
            :class:`PermissionOverwrite` to apply to the channel.
        default_auto_archive_duration: :class:`int`
            The new default auto archive duration in minutes for threads created in this channel.
            Must be one of ``60``, ``1440``, ``4320``, or ``10080``.

            .. versionadded:: 2.0
        default_thread_slowmode_delay: :class:`int`
            The new default slowmode delay in seconds for threads created in this channel.

            .. versionadded:: 2.3
        Raises
        ------
        ValueError
            The new ``position`` is less than 0 or greater than the number of channels.
        TypeError
            The permission overwrite information is not in proper form.
        Forbidden
            You do not have permissions to edit the channel.
        HTTPException
            Editing the channel failed.

        Returns
        --------
        Optional[:class:`.TextChannel`]
            The newly edited text channel. If the edit was only positional
            then ``None`` is returned instead.
        """

        payload = await self._edit(options, reason=reason)
        if payload is not None:
            # the payload will always be the proper channel payload
            return self.__class__(state=self._state, guild=self.guild, data=payload)  # type: ignore

    @utils.copy_doc(abc.GuildChannel.clone)
    async def clone(
        self,
        *,
        name: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        reason: Optional[str] = None,
    ) -> TextChannel:
        base: Dict[Any, Any] = {
            'topic': self.topic,
            'nsfw': self.nsfw,
            'default_auto_archive_duration': self.default_auto_archive_duration,
            'default_thread_rate_limit_per_user': self.default_thread_slowmode_delay,
        }
        if not self.is_news():
            base['rate_limit_per_user'] = self.slowmode_delay
        return await self._clone_impl(
            base,
            name=name,
            category=category,
            reason=reason,
        )

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

        .. versionchanged:: 2.0

            ``messages`` parameter is now positional-only.

            The ``reason`` keyword-only parameter was added.

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

        .. versionchanged:: 2.0

            The ``reason`` keyword-only parameter was added.

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

        .. versionchanged:: 1.1
            Added the ``reason`` keyword-only parameter.

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

    async def follow(self, *, destination: TextChannel, reason: Optional[str] = None) -> Webhook:
        """|coro|

        Follows a channel using a webhook.

        Only news channels can be followed.

        .. note::

            The webhook returned will not provide a token to do webhook
            actions, as Discord does not provide it.

        .. versionadded:: 1.3

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` instead of
            ``InvalidArgument``.

        Parameters
        -----------
        destination: :class:`TextChannel`
            The channel you would like to follow from.
        reason: Optional[:class:`str`]
            The reason for following the channel. Shows up on the destination guild's audit log.

            .. versionadded:: 1.4

        Raises
        -------
        HTTPException
            Following the channel failed.
        Forbidden
            You do not have the permissions to create a webhook.
        ClientException
            The channel is not a news channel.
        TypeError
            The destination channel is not a text channel.

        Returns
        --------
        :class:`Webhook`
            The created webhook.
        """

        if not self.is_news():
            raise ClientException('The channel must be a news channel.')

        if not isinstance(destination, TextChannel):
            raise TypeError(f'Expected TextChannel received {destination.__class__.__name__}')

        from ...webhook import Webhook

        data = await self._state.http.follow_webhook(self.id, webhook_channel_id=destination.id, reason=reason)
        return Webhook._as_follower(data, channel=destination, user=self._state.user)

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

        from ...message import PartialMessage

        return PartialMessage(channel=self, id=message_id)

    def get_thread(self, thread_id: int, /) -> Optional[Thread]:
        """Returns a thread with the given ID.

        .. note::

            This does not always retrieve archived threads, as they are not retained in the internal
            cache. Use :func:`Guild.fetch_channel` instead.

        .. versionadded:: 2.0

        Parameters
        -----------
        thread_id: :class:`int`
            The ID to search for.

        Returns
        --------
        Optional[:class:`Thread`]
            The returned thread or ``None`` if not found.
        """
        return self.guild.get_thread(thread_id)

    async def create_thread(
        self,
        *,
        name: str,
        message: Optional[Snowflake] = None,
        auto_archive_duration: ThreadArchiveDuration = MISSING,
        type: Optional[ChannelType] = None,
        reason: Optional[str] = None,
        invitable: bool = True,
        slowmode_delay: Optional[int] = None,
    ) -> Thread:
        """|coro|

        Creates a thread in this text channel.

        To create a public thread, you must have :attr:`~discord.Permissions.create_public_threads`.
        For a private thread, :attr:`~discord.Permissions.create_private_threads` is needed instead.

        .. versionadded:: 2.0

        Parameters
        -----------
        name: :class:`str`
            The name of the thread.
        message: Optional[:class:`abc.Snowflake`]
            A snowflake representing the message to create the thread with.
            If ``None`` is passed then a private thread is created.
            Defaults to ``None``.
        auto_archive_duration: :class:`int`
            The duration in minutes before a thread is automatically hidden from the channel list.
            If not provided, the channel's default auto archive duration is used.

            Must be one of ``60``, ``1440``, ``4320``, or ``10080``, if provided.
        type: Optional[:class:`ChannelType`]
            The type of thread to create. If a ``message`` is passed then this parameter
            is ignored, as a thread created with a message is always a public thread.
            By default this creates a private thread if this is ``None``.
        reason: :class:`str`
            The reason for creating a new thread. Shows up on the audit log.
        invitable: :class:`bool`
            Whether non-moderators can add users to the thread. Only applicable to private threads.
            Defaults to ``True``.
        slowmode_delay: Optional[:class:`int`]
            Specifies the slowmode rate limit for user in this channel, in seconds.
            The maximum value possible is ``21600``. By default no slowmode rate limit
            if this is ``None``.

        Raises
        -------
        Forbidden
            You do not have permissions to create a thread.
        HTTPException
            Starting the thread failed.

        Returns
        --------
        :class:`Thread`
            The created thread
        """

        if type is None:
            type = ChannelType.private_thread

        if message is None:
            data = await self._state.http.start_thread_without_message(
                self.id,
                name=name,
                auto_archive_duration=auto_archive_duration or self.default_auto_archive_duration,
                type=type.value,  # type: ignore # we're assuming that the user is passing a valid variant
                reason=reason,
                invitable=invitable,
                rate_limit_per_user=slowmode_delay,
            )
        else:
            data = await self._state.http.start_thread_with_message(
                self.id,
                message.id,
                name=name,
                auto_archive_duration=auto_archive_duration or self.default_auto_archive_duration,
                reason=reason,
                rate_limit_per_user=slowmode_delay,
            )

        return Thread(guild=self.guild, state=self._state, data=data)

    async def archived_threads(
        self,
        *,
        private: bool = False,
        joined: bool = False,
        limit: Optional[int] = 100,
        before: Optional[Union[Snowflake, datetime.datetime]] = None,
    ) -> AsyncIterator[Thread]:
        """Returns an :term:`asynchronous iterator` that iterates over all archived threads in this text channel,
        in order of decreasing ID for joined threads, and decreasing :attr:`Thread.archive_timestamp` otherwise.

        You must have :attr:`~Permissions.read_message_history` to do this. If iterating over private threads
        then :attr:`~Permissions.manage_threads` is also required.

        .. versionadded:: 2.0

        Parameters
        -----------
        limit: Optional[:class:`bool`]
            The number of threads to retrieve.
            If ``None``, retrieves every archived thread in the channel. Note, however,
            that this would make it a slow operation.
        before: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]
            Retrieve archived channels before the given date or ID.
        private: :class:`bool`
            Whether to retrieve private archived threads.
        joined: :class:`bool`
            Whether to retrieve private archived threads that you've joined.
            You cannot set ``joined`` to ``True`` and ``private`` to ``False``.

        Raises
        ------
        Forbidden
            You do not have permissions to get archived threads.
        HTTPException
            The request to get the archived threads failed.
        ValueError
            ``joined`` was set to ``True`` and ``private`` was set to ``False``. You cannot retrieve public archived
            threads that you have joined.

        Yields
        -------
        :class:`Thread`
            The archived threads.
        """
        if joined and not private:
            raise ValueError('Cannot retrieve joined public archived threads')

        before_timestamp = None

        if isinstance(before, datetime.datetime):
            if joined:
                before_timestamp = str(utils.time_snowflake(before, high=False))
            else:
                before_timestamp = before.isoformat()
        elif before is not None:
            if joined:
                before_timestamp = str(before.id)
            else:
                before_timestamp = utils.snowflake_time(before.id).isoformat()

        update_before = lambda data: data['thread_metadata']['archive_timestamp']
        endpoint = self.guild._state.http.get_public_archived_threads

        if joined:
            update_before = lambda data: data['id']
            endpoint = self.guild._state.http.get_joined_private_archived_threads
        elif private:
            endpoint = self.guild._state.http.get_private_archived_threads

        while True:
            retrieve = 100
            if limit is not None:
                if limit <= 0:
                    return
                retrieve = max(2, min(retrieve, limit))

            data = await endpoint(self.id, before=before_timestamp, limit=retrieve)

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
