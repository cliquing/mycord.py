
from ....utils.flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value

@fill_with_flags()
class SKUFlags(BaseFlags):
    r"""Wraps up the Discord SKU flags

    .. versionadded:: 2.4

    .. container:: operations

        .. describe:: x == y

            Checks if two SKUFlags are equal.

        .. describe:: x != y

            Checks if two SKUFlags are not equal.

        .. describe:: x | y, x |= y

            Returns a SKUFlags instance with all enabled flags from
            both x and y.

        .. describe:: x & y, x &= y

            Returns a SKUFlags instance with only flags enabled on
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns a SKUFlags instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns a SKUFlags instance with all flags inverted from x.

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
    def available(self):
        """:class:`bool`: Returns ``True`` if the SKU is available for purchase."""
        return 1 << 2

    @flag_value
    def guild_subscription(self):
        """:class:`bool`: Returns ``True`` if the SKU is a guild subscription."""
        return 1 << 7

    @flag_value
    def user_subscription(self):
        """:class:`bool`: Returns ``True`` if the SKU is a user subscription."""
        return 1 << 8
