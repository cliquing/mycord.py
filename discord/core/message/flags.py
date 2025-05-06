from ...utils.flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value


@fill_with_flags()
class MessageFlags(BaseFlags):
    r"""Wraps up a Discord Message flag value.

    See :class:`SystemChannelFlags`.

    .. container:: operations

        .. describe:: x == y

            Checks if two flags are equal.
        .. describe:: x != y

            Checks if two flags are not equal.

        .. describe:: x | y, x |= y

            Returns a MessageFlags instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns a MessageFlags instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns a MessageFlags instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns a MessageFlags instance with all flags inverted from x.

            .. versionadded:: 2.0

        .. describe:: hash(x)

               Return the flag's hash.
        .. describe:: iter(x)

               Returns an iterator of ``(name, value)`` pairs. This allows it
               to be, for example, constructed as a dict or a list of pairs.

        .. describe:: bool(b)

            Returns whether any flag is set to ``True``.

            .. versionadded:: 2.0

    .. versionadded:: 1.3

    Attributes
    -----------
    value: :class:`int`
        The raw value. This value is a bit array field of a 53-bit integer
        representing the currently available flags. You should query
        flags via the properties rather than using this raw value.
    """

    __slots__ = ()

    @flag_value
    def crossposted(self):
        """:class:`bool`: Returns ``True`` if the message is the original crossposted message."""
        return 1

    @flag_value
    def is_crossposted(self):
        """:class:`bool`: Returns ``True`` if the message was crossposted from another channel."""
        return 2

    @flag_value
    def suppress_embeds(self):
        """:class:`bool`: Returns ``True`` if the message's embeds have been suppressed."""
        return 4

    @flag_value
    def source_message_deleted(self):
        """:class:`bool`: Returns ``True`` if the source message for this crosspost has been deleted."""
        return 8

    @flag_value
    def urgent(self):
        """:class:`bool`: Returns ``True`` if the source message is an urgent message.

        An urgent message is one sent by Discord Trust and Safety.
        """
        return 16

    @flag_value
    def has_thread(self):
        """:class:`bool`: Returns ``True`` if the source message is associated with a thread.

        .. versionadded:: 2.0
        """
        return 32

    @flag_value
    def ephemeral(self):
        """:class:`bool`: Returns ``True`` if the source message is ephemeral.

        .. versionadded:: 2.0
        """
        return 64

    @flag_value
    def loading(self):
        """:class:`bool`: Returns ``True`` if the message is an interaction response and the bot
        is "thinking".

        .. versionadded:: 2.0
        """
        return 128

    @flag_value
    def failed_to_mention_some_roles_in_thread(self):
        """:class:`bool`: Returns ``True`` if the message failed to mention some roles in a thread
        and add their members to the thread.

        .. versionadded:: 2.0
        """
        return 256

    @flag_value
    def suppress_notifications(self):
        """:class:`bool`: Returns ``True`` if the message will not trigger push and desktop notifications.

        .. versionadded:: 2.2
        """
        return 4096

    @alias_flag_value
    def silent(self):
        """:class:`bool`: Alias for :attr:`suppress_notifications`.

        .. versionadded:: 2.2
        """
        return 4096

    @flag_value
    def voice(self):
        """:class:`bool`: Returns ``True`` if the message is a voice message.

        .. versionadded:: 2.3
        """
        return 8192

    @flag_value
    def forwarded(self):
        """:class:`bool`: Returns ``True`` if the message is a forwarded message.

        .. versionadded:: 2.5
        """
        return 16384


@fill_with_flags()
class AttachmentFlags(BaseFlags):
    r"""Wraps up the Discord Attachment flags

    .. versionadded:: 2.4

    .. container:: operations

        .. describe:: x == y

            Checks if two AttachmentFlags are equal.

        .. describe:: x != y

            Checks if two AttachmentFlags are not equal.

        .. describe:: x | y, x |= y

            Returns a AttachmentFlags instance with all enabled flags from
            both x and y.

        .. describe:: x & y, x &= y

            Returns a AttachmentFlags instance with only flags enabled on
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns a AttachmentFlags instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns a AttachmentFlags instance with all flags inverted from x.

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
    def clip(self):
        """:class:`bool`: Returns ``True`` if the attachment is a clip."""
        return 1 << 0

    @flag_value
    def thumbnail(self):
        """:class:`bool`: Returns ``True`` if the attachment is a thumbnail."""
        return 1 << 1

    @flag_value
    def remix(self):
        """:class:`bool`: Returns ``True`` if the attachment has been edited using the remix feature."""
        return 1 << 2

    @flag_value
    def spoiler(self):
        """:class:`bool`: Returns ``True`` if the attachment was marked as a spoiler.

        .. versionadded:: 2.5
        """
        return 1 << 3

    @flag_value
    def contains_explicit_media(self):
        """:class:`bool`: Returns ``True`` if the attachment was flagged as sensitive content.

        .. versionadded:: 2.5
        """
        return 1 << 4

    @flag_value
    def animated(self):
        """:class:`bool`: Returns ``True`` if the attachment is an animated image.

        .. versionadded:: 2.5
        """
        return 1 << 5
