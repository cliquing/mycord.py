from ..flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value


@fill_with_flags(inverted=True)
class SystemChannelFlags(BaseFlags):
    r"""Wraps up a Discord system channel flag value.

    Similar to :class:`Permissions`\, the properties provided are two way.
    You can set and retrieve individual bits using the properties as if they
    were regular bools. This allows you to edit the system flags easily.

    To construct an object you can pass keyword arguments denoting the flags
    to enable or disable.

    .. container:: operations

        .. describe:: x == y

            Checks if two flags are equal.

        .. describe:: x != y

            Checks if two flags are not equal.

        .. describe:: x | y, x |= y

            Returns a SystemChannelFlags instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns a SystemChannelFlags instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns a SystemChannelFlags instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns a SystemChannelFlags instance with all flags inverted from x.

            .. versionadded:: 2.0

        .. describe:: hash(x)

               Return the flag's hash.

        .. describe:: iter(x)

               Returns an iterator of ``(name, value)`` pairs. This allows it
               to be, for example, constructed as a dict or a list of pairs.

        .. describe:: bool(b)

            Returns whether any flag is set to ``True``.

            .. versionadded:: 2.0

    Attributes
    -----------
    value: :class:`int`
        The raw value. This value is a bit array field of a 53-bit integer
        representing the currently available flags. You should query
        flags via the properties rather than using this raw value.
    """

    __slots__ = ()

    # For some reason the flags for system channels are "inverted"
    # ergo, if they're set then it means "suppress" (off in the GUI toggle)
    # Since this is counter-intuitive from an API perspective and annoying
    # these will be inverted automatically

    def _has_flag(self, o: int) -> bool:
        return (self.value & o) != o

    def _set_flag(self, o: int, toggle: bool) -> None:
        if toggle is True:
            self.value &= ~o
        elif toggle is False:
            self.value |= o
        else:
            raise TypeError('Value to set for SystemChannelFlags must be a bool.')

    @flag_value
    def join_notifications(self):
        """:class:`bool`: Returns ``True`` if the system channel is used for member join notifications."""
        return 1

    @flag_value
    def premium_subscriptions(self):
        """:class:`bool`: Returns ``True`` if the system channel is used for "Nitro boosting" notifications."""
        return 2

    @flag_value
    def guild_reminder_notifications(self):
        """:class:`bool`: Returns ``True`` if the system channel is used for server setup helpful tips notifications.

        .. versionadded:: 2.0
        """
        return 4

    @flag_value
    def join_notification_replies(self):
        """:class:`bool`: Returns ``True`` if sticker reply button ("Wave to say hi!") is
        shown for member join notifications.

        .. versionadded:: 2.0
        """
        return 8

    @flag_value
    def role_subscription_purchase_notifications(self):
        """:class:`bool`: Returns ``True`` if role subscription purchase and renewal
        notifications are enabled.

        .. versionadded:: 2.2
        """
        return 16

    @flag_value
    def role_subscription_purchase_notification_replies(self):
        """:class:`bool`: Returns ``True`` if the role subscription notifications
        have a sticker reply button.

        .. versionadded:: 2.2
        """
        return 32




@fill_with_flags()
class ChannelFlags(BaseFlags):
    r"""Wraps up the Discord :class:`~discord.abc.GuildChannel` or :class:`Thread` flags.

    .. container:: operations

        .. describe:: x == y

            Checks if two channel flags are equal.
        .. describe:: x != y

            Checks if two channel flags are not equal.

        .. describe:: x | y, x |= y

            Returns a ChannelFlags instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns a ChannelFlags instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns a ChannelFlags instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns a ChannelFlags instance with all flags inverted from x.

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
    def pinned(self):
        """:class:`bool`: Returns ``True`` if the thread is pinned to the forum channel."""
        return 1 << 1

    @flag_value
    def require_tag(self):
        """:class:`bool`: Returns ``True`` if a tag is required to be specified when creating a thread
        in a :class:`ForumChannel`.

        .. versionadded:: 2.1
        """
        return 1 << 4

    @flag_value
    def hide_media_download_options(self):
        """:class:`bool`: Returns ``True`` if the client hides embedded media download options in a :class:`ForumChannel`.
        Only available in media channels.

        .. versionadded:: 2.4
        """
        return 1 << 15
