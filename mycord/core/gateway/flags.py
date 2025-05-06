from __future__ import annotations
from functools import reduce
from typing import Type
from ...utils.flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value



from typing import (
    TYPE_CHECKING,
)


if TYPE_CHECKING:
    pass
    
@fill_with_flags()
class Intents(BaseFlags):
    r"""Wraps up a Discord gateway intent flag.

    Similar to :class:`Permissions`\, the properties provided are two way.
    You can set and retrieve individual bits using the properties as if they
    were regular bools.

    To construct an object you can pass keyword arguments denoting the flags
    to enable or disable.

    This is used to disable certain gateway features that are unnecessary to
    run your bot. To make use of this, it is passed to the ``intents`` keyword
    argument of :class:`Client`.

    .. versionadded:: 1.5

    .. container:: operations

        .. describe:: x == y

            Checks if two flags are equal.
        .. describe:: x != y

            Checks if two flags are not equal.

        .. describe:: x | y, x |= y

            Returns an Intents instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns an Intents instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns an Intents instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns an Intents instance with all flags inverted from x.

            .. versionadded:: 2.0

        .. describe:: hash(x)

               Return the flag's hash.
        .. describe:: iter(x)

               Returns an iterator of ``(name, value)`` pairs. This allows it
               to be, for example, constructed as a dict or a list of pairs.

        .. describe:: bool(b)

            Returns whether any intent is enabled.

            .. versionadded:: 2.0

    Attributes
    -----------
    value: :class:`int`
        The raw value. You should query flags via the properties
        rather than using this raw value.
    """

    __slots__ = ()

    def __init__(self, value: int = 0, **kwargs: bool) -> None:
        self.value: int = value
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError(f'{key!r} is not a valid flag name.')
            setattr(self, key, value)

    @classmethod
    def all(cls: Type[Intents]) -> Intents:
        """A factory method that creates a :class:`Intents` with everything enabled."""
        value = reduce(lambda a, b: a | b, cls.VALID_FLAGS.values())
        self = cls.__new__(cls)
        self.value = value
        return self

    @classmethod
    def none(cls: Type[Intents]) -> Intents:
        """A factory method that creates a :class:`Intents` with everything disabled."""
        self = cls.__new__(cls)
        self.value = self.DEFAULT_VALUE
        return self

    @classmethod
    def default(cls: Type[Intents]) -> Intents:
        """A factory method that creates a :class:`Intents` with everything enabled
        except :attr:`presences`, :attr:`members`, and :attr:`message_content`.
        """
        self = cls.all()
        self.presences = False
        self.members = False
        self.message_content = False
        return self

    @flag_value
    def guilds(self):
        """:class:`bool`: Whether guild related events are enabled.

        This corresponds to the following events:

        - :func:`on_guild_join`
        - :func:`on_guild_remove`
        - :func:`on_guild_available`
        - :func:`on_guild_unavailable`
        - :func:`on_guild_channel_update`
        - :func:`on_guild_channel_create`
        - :func:`on_guild_channel_delete`
        - :func:`on_guild_channel_pins_update`
        - :func:`on_thread_create`
        - :func:`on_thread_join`
        - :func:`on_thread_update`
        - :func:`on_thread_delete`

        This also corresponds to the following attributes and classes in terms of cache:

        - :attr:`Client.guilds`
        - :class:`Guild` and all its attributes.
        - :meth:`Client.get_channel`
        - :meth:`Client.get_all_channels`

        It is highly advisable to leave this intent enabled for your bot to function.
        """
        return 1 << 0

    @flag_value
    def members(self):
        """:class:`bool`: Whether guild member related events are enabled.

        This corresponds to the following events:

        - :func:`on_member_join`
        - :func:`on_member_remove`
        - :func:`on_member_update`
        - :func:`on_user_update`
        - :func:`on_thread_member_join`
        - :func:`on_thread_member_remove`

        This also corresponds to the following attributes and classes in terms of cache:

        - :meth:`Client.get_all_members`
        - :meth:`Client.get_user`
        - :meth:`Guild.chunk`
        - :meth:`Guild.fetch_members`
        - :meth:`Guild.get_member`
        - :attr:`Guild.members`
        - :attr:`Member.roles`
        - :attr:`Member.nick`
        - :attr:`Member.premium_since`
        - :attr:`User.name`
        - :attr:`User.avatar`
        - :attr:`User.discriminator`
        - :attr:`User.global_name`

        For more information go to the :ref:`member intent documentation <need_members_intent>`.

        .. note::

            Currently, this requires opting in explicitly via the developer portal as well.
            Bots in over 100 guilds will need to apply to Discord for verification.
        """
        return 1 << 1

    @flag_value
    def moderation(self):
        """:class:`bool`: Whether guild moderation related events are enabled.

        This corresponds to the following events:

        - :func:`on_member_ban`
        - :func:`on_member_unban`
        - :func:`on_audit_log_entry_create`

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return 1 << 2

    @alias_flag_value
    def bans(self):
        """:class:`bool`: An alias of :attr:`moderation`.

        .. versionchanged:: 2.2
            Changed to an alias.
        """
        return 1 << 2

    @alias_flag_value
    def emojis(self):
        """:class:`bool`: Alias of :attr:`.expressions`.

        .. versionchanged:: 2.0
            Changed to an alias.
        """
        return 1 << 3

    @alias_flag_value
    def emojis_and_stickers(self):
        """:class:`bool`: Alias of :attr:`.expressions`.

        .. versionadded:: 2.0

        .. versionchanged:: 2.5
            Changed to an alias.
        """
        return 1 << 3

    @flag_value
    def expressions(self):
        """:class:`bool`: Whether guild emoji, sticker, and soundboard sound related events are enabled.

        .. versionadded:: 2.5

        This corresponds to the following events:

        - :func:`on_guild_emojis_update`
        - :func:`on_guild_stickers_update`
        - :func:`on_soundboard_sound_create`
        - :func:`on_soundboard_sound_update`
        - :func:`on_soundboard_sound_delete`

        This also corresponds to the following attributes and classes in terms of cache:

        - :class:`Emoji`
        - :class:`GuildSticker`
        - :class:`SoundboardSound`
        - :meth:`Client.get_emoji`
        - :meth:`Client.get_sticker`
        - :meth:`Client.get_soundboard_sound`
        - :meth:`Client.emojis`
        - :meth:`Client.stickers`
        - :meth:`Client.soundboard_sounds`
        - :attr:`Guild.emojis`
        - :attr:`Guild.stickers`
        - :attr:`Guild.soundboard_sounds`
        """
        return 1 << 3

    @flag_value
    def integrations(self):
        """:class:`bool`: Whether guild integration related events are enabled.

        This corresponds to the following events:

        - :func:`on_guild_integrations_update`
        - :func:`on_integration_create`
        - :func:`on_integration_update`
        - :func:`on_raw_integration_delete`

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return 1 << 4

    @flag_value
    def webhooks(self):
        """:class:`bool`: Whether guild webhook related events are enabled.

        This corresponds to the following events:

        - :func:`on_webhooks_update`

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return 1 << 5

    @flag_value
    def invites(self):
        """:class:`bool`: Whether guild invite related events are enabled.

        This corresponds to the following events:

        - :func:`on_invite_create`
        - :func:`on_invite_delete`

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return 1 << 6

    @flag_value
    def voice_states(self):
        """:class:`bool`: Whether guild voice state related events are enabled.

        This corresponds to the following events:

        - :func:`on_voice_state_update`

        This also corresponds to the following attributes and classes in terms of cache:

        - :attr:`VoiceChannel.members`
        - :attr:`VoiceChannel.voice_states`
        - :attr:`Member.voice`

        .. note::

            This intent is required to connect to voice.
        """
        return 1 << 7

    @flag_value
    def presences(self):
        """:class:`bool`: Whether guild presence related events are enabled.

        This corresponds to the following events:

        - :func:`on_presence_update`

        This also corresponds to the following attributes and classes in terms of cache:

        - :attr:`Member.activities`
        - :attr:`Member.status`
        - :attr:`Member.raw_status`

        For more information go to the :ref:`presence intent documentation <need_presence_intent>`.

        .. note::

            Currently, this requires opting in explicitly via the developer portal as well.
            Bots in over 100 guilds will need to apply to Discord for verification.
        """
        return 1 << 8

    @alias_flag_value
    def messages(self):
        """:class:`bool`: Whether guild and direct message related events are enabled.

        This is a shortcut to set or get both :attr:`guild_messages` and :attr:`dm_messages`.

        This corresponds to the following events:

        - :func:`on_message` (both guilds and DMs)
        - :func:`on_message_edit` (both guilds and DMs)
        - :func:`on_message_delete` (both guilds and DMs)
        - :func:`on_raw_message_delete` (both guilds and DMs)
        - :func:`on_raw_message_edit` (both guilds and DMs)

        This also corresponds to the following attributes and classes in terms of cache:

        - :class:`Message`
        - :attr:`Client.cached_messages`

        Note that due to an implicit relationship this also corresponds to the following events:

        - :func:`on_reaction_add` (both guilds and DMs)
        - :func:`on_reaction_remove` (both guilds and DMs)
        - :func:`on_reaction_clear` (both guilds and DMs)
        """
        return (1 << 9) | (1 << 12)

    @flag_value
    def guild_messages(self):
        """:class:`bool`: Whether guild message related events are enabled.

        See also :attr:`dm_messages` for DMs or :attr:`messages` for both.

        This corresponds to the following events:

        - :func:`on_message` (only for guilds)
        - :func:`on_message_edit` (only for guilds)
        - :func:`on_message_delete` (only for guilds)
        - :func:`on_raw_message_delete` (only for guilds)
        - :func:`on_raw_message_edit` (only for guilds)

        This also corresponds to the following attributes and classes in terms of cache:

        - :class:`Message`
        - :attr:`Client.cached_messages` (only for guilds)

        Note that due to an implicit relationship this also corresponds to the following events:

        - :func:`on_reaction_add` (only for guilds)
        - :func:`on_reaction_remove` (only for guilds)
        - :func:`on_reaction_clear` (only for guilds)
        """
        return 1 << 9

    @flag_value
    def dm_messages(self):
        """:class:`bool`: Whether direct message related events are enabled.

        See also :attr:`guild_messages` for guilds or :attr:`messages` for both.

        This corresponds to the following events:

        - :func:`on_message` (only for DMs)
        - :func:`on_message_edit` (only for DMs)
        - :func:`on_message_delete` (only for DMs)
        - :func:`on_raw_message_delete` (only for DMs)
        - :func:`on_raw_message_edit` (only for DMs)

        This also corresponds to the following attributes and classes in terms of cache:

        - :class:`Message`
        - :attr:`Client.cached_messages` (only for DMs)

        Note that due to an implicit relationship this also corresponds to the following events:

        - :func:`on_reaction_add` (only for DMs)
        - :func:`on_reaction_remove` (only for DMs)
        - :func:`on_reaction_clear` (only for DMs)
        """
        return 1 << 12

    @alias_flag_value
    def reactions(self):
        """:class:`bool`: Whether guild and direct message reaction related events are enabled.

        This is a shortcut to set or get both :attr:`guild_reactions` and :attr:`dm_reactions`.

        This corresponds to the following events:

        - :func:`on_reaction_add` (both guilds and DMs)
        - :func:`on_reaction_remove` (both guilds and DMs)
        - :func:`on_reaction_clear` (both guilds and DMs)
        - :func:`on_raw_reaction_add` (both guilds and DMs)
        - :func:`on_raw_reaction_remove` (both guilds and DMs)
        - :func:`on_raw_reaction_clear` (both guilds and DMs)

        This also corresponds to the following attributes and classes in terms of cache:

        - :attr:`Message.reactions` (both guild and DM messages)
        """
        return (1 << 10) | (1 << 13)

    @flag_value
    def guild_reactions(self):
        """:class:`bool`: Whether guild message reaction related events are enabled.

        See also :attr:`dm_reactions` for DMs or :attr:`reactions` for both.

        This corresponds to the following events:

        - :func:`on_reaction_add` (only for guilds)
        - :func:`on_reaction_remove` (only for guilds)
        - :func:`on_reaction_clear` (only for guilds)
        - :func:`on_raw_reaction_add` (only for guilds)
        - :func:`on_raw_reaction_remove` (only for guilds)
        - :func:`on_raw_reaction_clear` (only for guilds)

        This also corresponds to the following attributes and classes in terms of cache:

        - :attr:`Message.reactions` (only for guild messages)
        """
        return 1 << 10

    @flag_value
    def dm_reactions(self):
        """:class:`bool`: Whether direct message reaction related events are enabled.

        See also :attr:`guild_reactions` for guilds or :attr:`reactions` for both.

        This corresponds to the following events:

        - :func:`on_reaction_add` (only for DMs)
        - :func:`on_reaction_remove` (only for DMs)
        - :func:`on_reaction_clear` (only for DMs)
        - :func:`on_raw_reaction_add` (only for DMs)
        - :func:`on_raw_reaction_remove` (only for DMs)
        - :func:`on_raw_reaction_clear` (only for DMs)

        This also corresponds to the following attributes and classes in terms of cache:

        - :attr:`Message.reactions` (only for DM messages)
        """
        return 1 << 13

    @alias_flag_value
    def typing(self):
        """:class:`bool`: Whether guild and direct message typing related events are enabled.

        This is a shortcut to set or get both :attr:`guild_typing` and :attr:`dm_typing`.

        This corresponds to the following events:

        - :func:`on_typing` (both guilds and DMs)

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return (1 << 11) | (1 << 14)

    @flag_value
    def guild_typing(self):
        """:class:`bool`: Whether guild and direct message typing related events are enabled.

        See also :attr:`dm_typing` for DMs or :attr:`typing` for both.

        This corresponds to the following events:

        - :func:`on_typing` (only for guilds)

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return 1 << 11

    @flag_value
    def dm_typing(self):
        """:class:`bool`: Whether guild and direct message typing related events are enabled.

        See also :attr:`guild_typing` for guilds or :attr:`typing` for both.

        This corresponds to the following events:

        - :func:`on_typing` (only for DMs)

        This does not correspond to any attributes or classes in the library in terms of cache.
        """
        return 1 << 14

    @flag_value
    def message_content(self):
        """:class:`bool`: Whether message content, attachments, embeds and components will be available in messages
        which do not meet the following criteria:

        - The message was sent by the client
        - The message was sent in direct messages
        - The message mentions the client

        This applies to the following events:

        - :func:`on_message`
        - :func:`on_message_edit`
        - :func:`on_message_delete`
        - :func:`on_raw_message_edit`

        For more information go to the :ref:`message content intent documentation <need_message_content_intent>`.

        .. note::

            Currently, this requires opting in explicitly via the developer portal as well.
            Bots in over 100 guilds will need to apply to Discord for verification.

        .. versionadded:: 2.0
        """
        return 1 << 15

    @flag_value
    def guild_scheduled_events(self):
        """:class:`bool`: Whether guild scheduled event related events are enabled.

        This corresponds to the following events:

        - :func:`on_scheduled_event_create`
        - :func:`on_scheduled_event_update`
        - :func:`on_scheduled_event_delete`
        - :func:`on_scheduled_event_user_add`
        - :func:`on_scheduled_event_user_remove`

        .. versionadded:: 2.0
        """
        return 1 << 16

    @alias_flag_value
    def auto_moderation(self):
        """:class:`bool`: Whether auto moderation related events are enabled.

        This is a shortcut to set or get both :attr:`auto_moderation_configuration`
        and :attr:`auto_moderation_execution`.

        This corresponds to the following events:

        - :func:`on_automod_rule_create`
        - :func:`on_automod_rule_update`
        - :func:`on_automod_rule_delete`
        - :func:`on_automod_action`

        .. versionadded:: 2.0
        """
        return (1 << 20) | (1 << 21)

    @flag_value
    def auto_moderation_configuration(self):
        """:class:`bool`: Whether auto moderation configuration related events are enabled.

        This corresponds to the following events:

        - :func:`on_automod_rule_create`
        - :func:`on_automod_rule_update`
        - :func:`on_automod_rule_delete`

        .. versionadded:: 2.0
        """
        return 1 << 20

    @flag_value
    def auto_moderation_execution(self):
        """:class:`bool`: Whether auto moderation execution related events are enabled.

        This corresponds to the following events:
        - :func:`on_automod_action`

        .. versionadded:: 2.0
        """
        return 1 << 21

    @alias_flag_value
    def polls(self):
        """:class:`bool`: Whether guild and direct messages poll related events are enabled.

        This is a shortcut to set or get both :attr:`guild_polls` and :attr:`dm_polls`.

        This corresponds to the following events:

        - :func:`on_poll_vote_add` (both guilds and DMs)
        - :func:`on_poll_vote_remove` (both guilds and DMs)
        - :func:`on_raw_poll_vote_add` (both guilds and DMs)
        - :func:`on_raw_poll_vote_remove` (both guilds and DMs)

        .. versionadded:: 2.4
        """
        return (1 << 24) | (1 << 25)

    @flag_value
    def guild_polls(self):
        """:class:`bool`: Whether guild poll related events are enabled.

        See also :attr:`dm_polls` and :attr:`polls`.

        This corresponds to the following events:

        - :func:`on_poll_vote_add` (only for guilds)
        - :func:`on_poll_vote_remove` (only for guilds)
        - :func:`on_raw_poll_vote_add` (only for guilds)
        - :func:`on_raw_poll_vote_remove` (only for guilds)

        .. versionadded:: 2.4
        """
        return 1 << 24

    @flag_value
    def dm_polls(self):
        """:class:`bool`: Whether direct messages poll related events are enabled.

        See also :attr:`guild_polls` and :attr:`polls`.

        This corresponds to the following events:

        - :func:`on_poll_vote_add` (only for DMs)
        - :func:`on_poll_vote_remove` (only for DMs)
        - :func:`on_raw_poll_vote_add` (only for DMs)
        - :func:`on_raw_poll_vote_remove` (only for DMs)

        .. versionadded:: 2.4
        """
        return 1 << 25
