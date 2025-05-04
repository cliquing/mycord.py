from __future__ import annotations

from typing import Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired

from ..scheduled_event.types import GuildScheduledEvent
from ....utils.snowflake import Snowflake
from ..types import InviteGuildPayload, _GuildPreviewUnique
from ..channel.types import PartialChannelPayload
from ...user.types import PartialUserPayload
from ...appinfo.types import PartialAppInfoPayload

InviteTargetType = Literal[1, 2]
InviteType = Literal[0, 1, 2]


class _InviteMetadata(TypedDict, total=False):
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: str
    expires_at: Optional[str]


class VanityInvite(_InviteMetadata):
    code: Optional[str]
    revoked: NotRequired[bool]


class IncompleteInvite(_InviteMetadata):
    code: str
    channel: PartialChannelPayload


class InvitePayload(IncompleteInvite, total=False):
    guild: InviteGuildPayload
    inviter: PartialUserPayload
    target_user: PartialUserPayload
    target_type: InviteTargetType
    target_application: PartialAppInfoPayload
    guild_scheduled_event: GuildScheduledEvent
    type: InviteType


class InviteWithCounts(InvitePayload, _GuildPreviewUnique):
    ...


class GatewayInviteCreate(TypedDict):
    channel_id: Snowflake
    code: str
    created_at: str
    max_age: int
    max_uses: int
    temporary: bool
    uses: bool
    guild_id: Snowflake
    inviter: NotRequired[PartialUserPayload]
    target_type: NotRequired[InviteTargetType]
    target_user: NotRequired[PartialUserPayload]
    target_application: NotRequired[PartialAppInfoPayload]


class GatewayInviteDelete(TypedDict):
    channel_id: Snowflake
    code: str
    guild_id: NotRequired[Snowflake]


GatewayInvitePayload = Union[GatewayInviteCreate, GatewayInviteDelete]
