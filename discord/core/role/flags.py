from ..flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value


@fill_with_flags()
class RoleFlags(BaseFlags):
    r"""Wraps up the Discord Role flags

    .. versionadded:: 2.4

    .. container:: operations

        .. describe:: x == y

            Checks if two RoleFlags are equal.

        .. describe:: x != y

            Checks if two RoleFlags are not equal.

        .. describe:: x | y, x |= y

            Returns a RoleFlags instance with all enabled flags from
            both x and y.

        .. describe:: x & y, x &= y

            Returns a RoleFlags instance with only flags enabled on
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns a RoleFlags instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns a RoleFlags instance with all flags inverted from x.

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
    def in_prompt(self):
        """:class:`bool`: Returns ``True`` if the role can be selected by members in an onboarding prompt."""
        return 1 << 0
