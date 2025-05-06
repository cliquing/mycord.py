from __future__ import annotations

from typing import TypedDict, Optional
from typing_extensions import NotRequired

from ....utils.snowflake import Snowflake


class RolePayload(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    flags: int
    icon: NotRequired[Optional[str]]
    unicode_emoji: NotRequired[Optional[str]]
    tags: NotRequired[RoleTagsPayload]


class RoleTagsPayload(TypedDict, total=False):
    bot_id: Snowflake
    integration_id: Snowflake
    subscription_listing_id: Snowflake
    premium_subscriber: None
    available_for_purchase: None
    guild_connections: None
