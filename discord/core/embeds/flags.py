from ..flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value


@fill_with_flags()
class EmbedFlags(BaseFlags):
    r"""Wraps up the Discord Embed flags

    .. versionadded:: 2.5

    .. container:: operations

        .. describe:: x == y

            Checks if two EmbedFlags are equal.

        .. describe:: x != y

            Checks if two EmbedFlags are not equal.

        .. describe:: x | y, x |= y

            Returns an EmbedFlags instance with all enabled flags from
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns an EmbedFlags instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns an EmbedFlags instance with all flags inverted from x.

        .. describe:: hash(x)

            Returns the flag's hash.

        .. describe:: iter(x)

            Returns an iterator of ``(name, value)`` pairs. This allows it
            to be, for example, constructed as a dict or a list of pairs.
            Note that aliases are not shown.

        .. describe:: bool(b)

            Returns whether any flag is set to ``True``.

    Attributes
    ----------
    value: :class:`int`
        The raw value. You should query flags via the properties
        rather than using this raw value.
    """

    @flag_value
    def contains_explicit_media(self):
        """:class:`bool`: Returns ``True`` if the embed was flagged as sensitive content."""
        return 1 << 4

    @flag_value
    def content_inventory_entry(self):
        """:class:`bool`: Returns ``True`` if the embed is a reply to an activity card, and is no
        longer displayed.
        """
        return 1 << 5
