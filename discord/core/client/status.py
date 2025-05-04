from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from .activity.activity import create_activity
from ...utils.utils import MISSING, _get_as_snowflake, _RawReprMixin
from ...utils.enums import try_enum
from .enums import Status
if TYPE_CHECKING:
    from typing_extensions import Self

    from .activity.activity import ActivityTypes
    from ..guild.guild import Guild
    from ..state.state import ConnectionState
    from .activity.types import ClientStatusPayload, PartialPresenceUpdate


__all__ = (
    'RawPresenceUpdateEvent',
    'ClientStatus',
)


class ClientStatus:
    """Represents the :ddocs:`Client Status Object <events/gateway-events#client-status-object>` from Discord,
    which holds information about the status of the user on various clients/platforms, with additional helpers.

    .. versionadded:: 2.5
    """

    __slots__ = ('_status', 'desktop', 'mobile', 'web')

    def __init__(self, *, status: str = MISSING, data: ClientStatusPayload = MISSING) -> None:
        self._status: str = status or 'offline'

        data = data or {}
        self.desktop: Optional[str] = data.get('desktop')
        self.mobile: Optional[str] = data.get('mobile')
        self.web: Optional[str] = data.get('web')

    def __repr__(self) -> str:
        attrs = [
            ('_status', self._status),
            ('desktop', self.desktop),
            ('mobile', self.mobile),
            ('web', self.web),
        ]
        inner = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {inner}>'

    def _update(self, status: str, data: ClientStatusPayload, /) -> None:
        self._status = status

        self.desktop = data.get('desktop')
        self.mobile = data.get('mobile')
        self.web = data.get('web')

    @classmethod
    def _copy(cls, client_status: Self, /) -> Self:
        self = cls.__new__(cls)  # bypass __init__

        self._status = client_status._status

        self.desktop = client_status.desktop
        self.mobile = client_status.mobile
        self.web = client_status.web

        return self

    @property
    def status(self) -> Status:
        """:class:`Status`: The user's overall status. If the value is unknown, then it will be a :class:`str` instead."""
        return try_enum(Status, self._status)

    @property
    def raw_status(self) -> str:
        """:class:`str`: The user's overall status as a string value."""
        return self._status

    @property
    def mobile_status(self) -> Status:
        """:class:`Status`: The user's status on a mobile device, if applicable."""
        return try_enum(Status, self.mobile or 'offline')

    @property
    def desktop_status(self) -> Status:
        """:class:`Status`: The user's status on the desktop client, if applicable."""
        return try_enum(Status, self.desktop or 'offline')

    @property
    def web_status(self) -> Status:
        """:class:`Status`: The user's status on the web client, if applicable."""
        return try_enum(Status, self.web or 'offline')

    def is_on_mobile(self) -> bool:
        """:class:`bool`: A helper function that determines if a user is active on a mobile device."""
        return self.mobile is not None