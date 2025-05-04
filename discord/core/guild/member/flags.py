from typing import Type
from ....utils.flags import BaseFlags, fill_with_flags, flag_value, alias_flag_value

__all__ = (

    'MemberCacheFlags',
    'MemberFlags',

)
from __future__ import annotations

from functools import reduce
from operator import or_
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    overload,
)


if TYPE_CHECKING:
    from typing_extensions import Self
    from ...gateway.flags import Intents

@fill_with_flags()
class MemberFlags(BaseFlags):
    r"""Wraps up the Discord Guild Member flags

    .. versionadded:: 2.2

    .. container:: operations

        .. describe:: x == y

            Checks if two MemberFlags are equal.

        .. describe:: x != y

            Checks if two MemberFlags are not equal.

        .. describe:: x | y, x |= y

            Returns a MemberFlags instance with all enabled flags from
            both x and y.

        .. describe:: x & y, x &= y

            Returns a MemberFlags instance with only flags enabled on
            both x and y.

        .. describe:: x ^ y, x ^= y

            Returns a MemberFlags instance with only flags enabled on
            only one of x or y, not on both.

        .. describe:: ~x

            Returns a MemberFlags instance with all flags inverted from x.

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
    def did_rejoin(self):
        """:class:`bool`: Returns ``True`` if the member left and rejoined the :attr:`~discord.Member.guild`."""
        return 1 << 0

    @flag_value
    def completed_onboarding(self):
        """:class:`bool`: Returns ``True`` if the member has completed onboarding."""
        return 1 << 1

    @flag_value
    def bypasses_verification(self):
        """:class:`bool`: Returns ``True`` if the member can bypass the guild verification requirements."""
        return 1 << 2

    @flag_value
    def started_onboarding(self):
        """:class:`bool`: Returns ``True`` if the member has started onboarding."""
        return 1 << 3

    @flag_value
    def guest(self):
        """:class:`bool`: Returns ``True`` if the member is a guest and can only access
        the voice channel they were invited to.

        .. versionadded:: 2.5
        """
        return 1 << 4

    @flag_value
    def started_home_actions(self):
        """:class:`bool`: Returns ``True`` if the member has started Server Guide new member actions.

        .. versionadded:: 2.5
        """
        return 1 << 5

    @flag_value
    def completed_home_actions(self):
        """:class:`bool`: Returns ``True`` if the member has completed Server Guide new member actions.

        .. versionadded:: 2.5
        """
        return 1 << 6

    @flag_value
    def automod_quarantined_username(self):
        """:class:`bool`: Returns ``True`` if the member's username, nickname, or global name has been
        blocked by AutoMod.

        .. versionadded:: 2.5
        """
        return 1 << 7

    @flag_value
    def dm_settings_upsell_acknowledged(self):
        """:class:`bool`: Returns ``True`` if the member has dismissed the DM settings upsell.

        .. versionadded:: 2.5
        """
        return 1 << 9



@fill_with_flags()
class MemberCacheFlags(BaseFlags):
    """Controls the library's cache policy when it comes to members.

    This allows for finer grained control over what members are cached.
    Note that the bot's own member is always cached. This class is passed
    to the ``member_cache_flags`` parameter in :class:`Client`.

    Due to a quirk in how Discord works, in order to ensure proper cleanup
    of cache resources it is recommended to have :attr:`Intents.members`
    enabled. Otherwise the library cannot know when a member leaves a guild and
    is thus unable to cleanup after itself.

    To construct an object you can pass keyword arguments denoting the flags
    to enable or disable.

    The default value is all flags enabled.

    .. versionadded:: 1.5

    .. container:: operations

        .. describe:: x == y

            Checks if two flags are equal.
        .. describe:: x != y

            Checks if two flags are not equal.

        .. describe:: x | y, x |= y

            Returns a MemberCacheFlags instance with all enabled flags from
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x & y, x &= y

            Returns a MemberCacheFlags instance with only flags enabled on
            both x and y.

            .. versionadded:: 2.0

        .. describe:: x ^ y, x ^= y

            Returns a MemberCacheFlags instance with only flags enabled on
            only one of x or y, not on both.

            .. versionadded:: 2.0

        .. describe:: ~x

            Returns a MemberCacheFlags instance with all flags inverted from x.

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
        The raw value. You should query flags via the properties
        rather than using this raw value.
    """

    __slots__ = ()

    def __init__(self, **kwargs: bool):
        bits = max(self.VALID_FLAGS.values()).bit_length()
        self.value: int = (1 << bits) - 1
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError(f'{key!r} is not a valid flag name.')
            setattr(self, key, value)

    @classmethod
    def all(cls: Type[MemberCacheFlags]) -> MemberCacheFlags:
        """A factory method that creates a :class:`MemberCacheFlags` with everything enabled."""
        bits = max(cls.VALID_FLAGS.values()).bit_length()
        value = (1 << bits) - 1
        self = cls.__new__(cls)
        self.value = value
        return self

    @classmethod
    def none(cls: Type[MemberCacheFlags]) -> MemberCacheFlags:
        """A factory method that creates a :class:`MemberCacheFlags` with everything disabled."""
        self = cls.__new__(cls)
        self.value = self.DEFAULT_VALUE
        return self

    @property
    def _empty(self):
        return self.value == self.DEFAULT_VALUE

    @flag_value
    def voice(self):
        """:class:`bool`: Whether to cache members that are in voice.

        This requires :attr:`Intents.voice_states`.

        Members that leave voice are no longer cached.
        """
        return 1

    @flag_value
    def joined(self):
        """:class:`bool`: Whether to cache members that joined the guild
        or are chunked as part of the initial log in flow.

        This requires :attr:`Intents.members`.

        Members that leave the guild are no longer cached.
        """
        return 2

    @classmethod
    def from_intents(cls: Type[MemberCacheFlags], intents: 'Intents') -> MemberCacheFlags:
        """A factory method that creates a :class:`MemberCacheFlags` based on
        the currently selected :class:`Intents`.

        Parameters
        ------------
        intents: :class:`Intents`
            The intents to select from.

        Returns
        ---------
        :class:`MemberCacheFlags`
            The resulting member cache flags.
        """

        self = cls.none()
        if intents.members:
            self.joined = True
        if intents.voice_states:
            self.voice = True

        return self

    def _verify_intents(self, intents: 'Intents'):
        if self.voice and not intents.voice_states:
            raise ValueError('MemberCacheFlags.voice requires Intents.voice_states')

        if self.joined and not intents.members:
            raise ValueError('MemberCacheFlags.joined requires Intents.members')

    @property
    def _voice_only(self):
        return self.value == 1


