from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ....utils.utils import _RawReprMixin
if TYPE_CHECKING:

    from .types import IntegrationDeleteEvent
    




__all__ = ('RawIntegrationDeleteEvent',
)

class RawIntegrationDeleteEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_integration_delete` event.

    .. versionadded:: 2.0

    Attributes
    -----------
    integration_id: :class:`int`
        The ID of the integration that got deleted.
    application_id: Optional[:class:`int`]
        The ID of the bot/OAuth2 application for this deleted integration.
    guild_id: :class:`int`
        The guild ID where the integration got deleted.
    """

    __slots__ = ('integration_id', 'application_id', 'guild_id')

    def __init__(self, data: IntegrationDeleteEvent) -> None:
        self.integration_id: int = int(data['id'])
        self.guild_id: int = int(data['guild_id'])

        try:
            self.application_id: Optional[int] = int(
                data['application_id']  # pyright: ignore[reportTypedDictNotRequiredAccess]
            )
        except KeyError:
            self.application_id: Optional[int] = None
