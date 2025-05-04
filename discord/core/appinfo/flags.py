from ...utils.flags import BaseFlags, ArrayFlags, fill_with_flags, flag_value, alias_flag_value

@fill_with_flags()
class ApplicationFlags(BaseFlags):
    r"""Wraps up the Discord Application flags.

    .. container:: operations

        .. describe:: x == y

            Checks if two ApplicationFlags are equal.
        .. describe:: x != y

            Checks if two ApplicationFlags are not equal.

        .. describe:: x | y, x |= y

            Returns an ApplicationFlags instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns an ApplicationFlags instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns an ApplicationFlags instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns an ApplicationFlags instance with all flags inverted from x.

            .. versionadded:: 2.0

        .. describe:: hash(x)

            Return the flag's hash.
        .. describe:: iter(x)

            Returns an iterator of ``(name, value)`` pairs. This allows it
            to be, for example, constructed as a dict or a list of pairs.
            Note that aliases are not shown.

        .. describe:: bool(b)

            Returns whether any flag is set to ``True``.

    .. versionadded:: 2.0

    Attributes
    -----------
    value: :class:`int`
        The raw value. You should query flags via the properties
        rather than using this raw value.
    """

    @flag_value
    def auto_mod_badge(self):
        """:class:`bool`: Returns ``True`` if the application uses at least 100 automod rules across all guilds.
        This shows up as a badge in the official client.

        .. versionadded:: 2.3
        """
        return 1 << 6

    @flag_value
    def gateway_presence(self):
        """:class:`bool`: Returns ``True`` if the application is verified and is allowed to
        receive presence information over the gateway.
        """
        return 1 << 12

    @flag_value
    def gateway_presence_limited(self):
        """:class:`bool`: Returns ``True`` if the application is allowed to receive limited
        presence information over the gateway.
        """
        return 1 << 13

    @flag_value
    def gateway_guild_members(self):
        """:class:`bool`: Returns ``True`` if the application is verified and is allowed to
        receive guild members information over the gateway.
        """
        return 1 << 14

    @flag_value
    def gateway_guild_members_limited(self):
        """:class:`bool`: Returns ``True`` if the application is allowed to receive limited
        guild members information over the gateway.
        """
        return 1 << 15

    @flag_value
    def verification_pending_guild_limit(self):
        """:class:`bool`: Returns ``True`` if the application is currently pending verification
        and has hit the guild limit.
        """
        return 1 << 16

    @flag_value
    def embedded(self):
        """:class:`bool`: Returns ``True`` if the application is embedded within the Discord client."""
        return 1 << 17

    @flag_value
    def gateway_message_content(self):
        """:class:`bool`: Returns ``True`` if the application is verified and is allowed to
        read message content in guilds."""
        return 1 << 18

    @flag_value
    def gateway_message_content_limited(self):
        """:class:`bool`: Returns ``True`` if the application is unverified and is allowed to
        read message content in guilds."""
        return 1 << 19

    @flag_value
    def app_commands_badge(self):
        """:class:`bool`: Returns ``True`` if the application has registered a global application
        command. This shows up as a badge in the official client."""
        return 1 << 23

    @flag_value
    def active(self):
        """:class:`bool`: Returns ``True`` if the application has had at least one global application
        command used in the last 30 days.

        .. versionadded:: 2.1
        """
        return 1 << 24


@fill_with_flags()
class AppCommandContext(ArrayFlags):
    r"""Wraps up the Discord :class:`~discord.app_commands.Command` execution context.

    .. versionadded:: 2.4

    .. container:: operations

        .. describe:: x == y

            Checks if two AppCommandContext flags are equal.

        .. describe:: x != y

            Checks if two AppCommandContext flags are not equal.

        .. describe:: x | y, x |= y

            Returns an AppCommandContext instance with all enabled flags from
            both x and y.

        .. describe:: x & y, x &= y

            Returns an AppCommandContext instance with only flags enabled on
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns an AppCommandContext instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns an AppCommandContext instance with all flags inverted from x

        .. describe:: hash(x)

            Return the flag's hash.
        .. describe:: iter(x)

            Returns an iterator of ``(name, value)`` pairs. This allows it
            to be, for example, constructed as a dict or a list of pairs.
            Note that aliases are not shown.

        .. describe:: bool(b)

            Returns whether any flag is set to ``True``.

    Attributes
    -----------
    value: :class:`int`
        The raw value. You should query flags via the properties
        rather than using this raw value.
    """

    DEFAULT_VALUE = 3

    @flag_value
    def guild(self):
        """:class:`bool`: Whether the context allows usage in a guild."""
        return 1 << 0

    @flag_value
    def dm_channel(self):
        """:class:`bool`: Whether the context allows usage in a DM channel."""
        return 1 << 1

    @flag_value
    def private_channel(self):
        """:class:`bool`: Whether the context allows usage in a DM or a GDM channel."""
        return 1 << 2


@fill_with_flags()
class AppInstallationType(ArrayFlags):
    r"""Represents the installation location of an application command.

    .. versionadded:: 2.4

    .. container:: operations

        .. describe:: x == y

            Checks if two AppInstallationType flags are equal.

        .. describe:: x != y

            Checks if two AppInstallationType flags are not equal.

        .. describe:: x | y, x |= y

            Returns an AppInstallationType instance with all enabled flags from
            both x and y.

        .. describe:: x & y, x &= y

            Returns an AppInstallationType instance with only flags enabled on
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns an AppInstallationType instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns an AppInstallationType instance with all flags inverted from x

        .. describe:: hash(x)

            Return the flag's hash.
        .. describe:: iter(x)

            Returns an iterator of ``(name, value)`` pairs. This allows it
            to be, for example, constructed as a dict or a list of pairs.
            Note that aliases are not shown.

        .. describe:: bool(b)

            Returns whether any flag is set to ``True``.

    Attributes
    -----------
    value: :class:`int`
        The raw value. You should query flags via the properties
        rather than using this raw value.
    """

    @flag_value
    def guild(self):
        """:class:`bool`: Whether the integration is a guild install."""
        return 1 << 0

    @flag_value
    def user(self):
        """:class:`bool`: Whether the integration is a user install."""
        return 1 << 1


