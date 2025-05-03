from ..flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value
from .enums import UserFlags


@fill_with_flags()
class PublicUserFlags(BaseFlags):
    r"""Wraps up the Discord User Public flags.

    .. container:: operations

        .. describe:: x == y

            Checks if two PublicUserFlags are equal.
        .. describe:: x != y

            Checks if two PublicUserFlags are not equal.

        .. describe:: x | y, x |= y

            Returns a PublicUserFlags instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns a PublicUserFlags instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns a PublicUserFlags instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns a PublicUserFlags instance with all flags inverted from x.

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

    .. versionadded:: 1.4

    Attributes
    -----------
    value: :class:`int`
        The raw value. This value is a bit array field of a 53-bit integer
        representing the currently available flags. You should query
        flags via the properties rather than using this raw value.
    """

    __slots__ = ()

    @flag_value
    def staff(self):
        """:class:`bool`: Returns ``True`` if the user is a Discord Employee."""
        return UserFlags.staff.value

    @flag_value
    def partner(self):
        """:class:`bool`: Returns ``True`` if the user is a Discord Partner."""
        return UserFlags.partner.value

    @flag_value
    def hypesquad(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Events member."""
        return UserFlags.hypesquad.value

    @flag_value
    def bug_hunter(self):
        """:class:`bool`: Returns ``True`` if the user is a Bug Hunter"""
        return UserFlags.bug_hunter.value

    @flag_value
    def hypesquad_bravery(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Bravery member."""
        return UserFlags.hypesquad_bravery.value

    @flag_value
    def hypesquad_brilliance(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Brilliance member."""
        return UserFlags.hypesquad_brilliance.value

    @flag_value
    def hypesquad_balance(self):
        """:class:`bool`: Returns ``True`` if the user is a HypeSquad Balance member."""
        return UserFlags.hypesquad_balance.value

    @flag_value
    def early_supporter(self):
        """:class:`bool`: Returns ``True`` if the user is an Early Supporter."""
        return UserFlags.early_supporter.value

    @flag_value
    def team_user(self):
        """:class:`bool`: Returns ``True`` if the user is a Team User."""
        return UserFlags.team_user.value

    @flag_value
    def system(self):
        """:class:`bool`: Returns ``True`` if the user is a system user (i.e. represents Discord officially)."""
        return UserFlags.system.value

    @flag_value
    def bug_hunter_level_2(self):
        """:class:`bool`: Returns ``True`` if the user is a Bug Hunter Level 2"""
        return UserFlags.bug_hunter_level_2.value

    @flag_value
    def verified_bot(self):
        """:class:`bool`: Returns ``True`` if the user is a Verified Bot."""
        return UserFlags.verified_bot.value

    @flag_value
    def verified_bot_developer(self):
        """:class:`bool`: Returns ``True`` if the user is an Early Verified Bot Developer."""
        return UserFlags.verified_bot_developer.value

    @alias_flag_value
    def early_verified_bot_developer(self):
        """:class:`bool`: An alias for :attr:`verified_bot_developer`.

        .. versionadded:: 1.5
        """
        return UserFlags.verified_bot_developer.value

    @flag_value
    def discord_certified_moderator(self):
        """:class:`bool`: Returns ``True`` if the user is a Discord Certified Moderator.

        .. versionadded:: 2.0
        """
        return UserFlags.discord_certified_moderator.value

    @flag_value
    def bot_http_interactions(self):
        """:class:`bool`: Returns ``True`` if the user is a bot that only uses HTTP interactions
        and is shown in the online member list.

        .. versionadded:: 2.0
        """
        return UserFlags.bot_http_interactions.value

    @flag_value
    def spammer(self):
        """:class:`bool`: Returns ``True`` if the user is flagged as a spammer by Discord.

        .. versionadded:: 2.0
        """
        return UserFlags.spammer.value

    @flag_value
    def active_developer(self):
        """:class:`bool`: Returns ``True`` if the user is an active developer.

        .. versionadded:: 2.1
        """
        return UserFlags.active_developer.value

    def all(self) -> List[UserFlags]:
        """List[:class:`UserFlags`]: Returns all public flags the user has."""
        return [public_flag for public_flag in UserFlags if self._has_flag(public_flag.value)]
