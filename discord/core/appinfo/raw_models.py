from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional, Set, List, Union


from ...utils.utils import _get_as_snowflake, _RawReprMixin
from ...app_commands import AppCommandPermissions

if TYPE_CHECKING:
    from typing_extensions import Self

    from ...types.command import GuildApplicationCommandPermissions

    from ...core.state import ConnectionState

    from ...core.guild.guild import Guild


__all__ = ('RawAppCommandPermissionsUpdateEvent',
)

class RawAppCommandPermissionsUpdateEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_app_command_permissions_update` event.

    .. versionadded:: 2.0

    Attributes
    ----------
    target_id: :class:`int`
        The ID of the command or application whose permissions were updated.
        When this is the application ID instead of a command ID, the permissions
        apply to all commands that do not contain explicit overwrites.
    application_id: :class:`int`
        The ID of the application that the command belongs to.
    guild: :class:`~discord.Guild`
        The guild where the permissions were updated.
    permissions: List[:class:`~discord.app_commands.AppCommandPermissions`]
        List of new permissions for the app command.
    """

    __slots__ = ('target_id', 'application_id', 'guild', 'permissions')

    def __init__(self, *, data: GuildApplicationCommandPermissions, state: ConnectionState):
        self.target_id: int = int(data['id'])
        self.application_id: int = int(data['application_id'])
        self.guild: Guild = state._get_or_create_unavailable_guild(int(data['guild_id']))
        self.permissions: List[AppCommandPermissions] = [
            AppCommandPermissions(data=perm, guild=self.guild, state=state) for perm in data['permissions']
        ]