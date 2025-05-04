from __future__ import annotations

from typing import Literal, Optional, TypedDict
from typing_extensions import NotRequired

from ...utils.snowflake import Snowflake
from ..user import User
from ..guild.channel.types import PartialChannelPayload


class SourceGuildPayload(TypedDict):
    id: int
    name: str
    icon: str


WebhookType = Literal[1, 2, 3]

class FollowerWebhookPayload(TypedDict):
    channel_id: Snowflake
    webhook_id: Snowflake
    source_channel: NotRequired[PartialChannelPayload]
    source_guild: NotRequired[SourceGuildPayload]


class PartialWebhookPayload(TypedDict):
    id: Snowflake
    type: WebhookType
    guild_id: NotRequired[Snowflake]
    user: NotRequired[User]
    token: NotRequired[str]


class _FullWebhook(TypedDict, total=False):
    name: Optional[str]
    avatar: Optional[str]
    channel_id: Snowflake
    application_id: Optional[Snowflake]


class WebhookPayload(PartialWebhookPayload, _FullWebhook):
    ...
