from typing import List
from ...core.flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value, ArrayFlags


@fill_with_flags()
class AutoModPresets(ArrayFlags):
    r"""Wraps up the Discord :class:`AutoModRule` presets.

    .. versionadded:: 2.0


    .. container:: operations

        .. describe:: x == y

            Checks if two AutoMod preset flags are equal.

        .. describe:: x != y

            Checks if two AutoMod preset flags are not equal.

        .. describe:: x | y, x |= y

            Returns an AutoModPresets instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns an AutoModPresets instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns an AutoModPresets instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns an AutoModPresets instance with all flags inverted from x.

            .. versionadded:: 2.0

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

    def to_array(self) -> List[int]:
        return super().to_array(offset=1)

    @flag_value
    def profanity(self):
        """:class:`bool`: Whether to use the preset profanity filter."""
        return 1 << 0

    @flag_value
    def sexual_content(self):
        """:class:`bool`: Whether to use the preset sexual content filter."""
        return 1 << 1

    @flag_value
    def slurs(self):
        """:class:`bool`: Whether to use the preset slurs filter."""
        return 1 << 2
