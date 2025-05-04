from __future__ import annotations

from typing import List, Literal, Optional, TypedDict


from ....utils.snowflake import Snowflake

SubscriptionStatus = Literal[0, 1, 2]

class SubscriptionPayload(TypedDict):
    id: Snowflake
    user_id: Snowflake
    sku_ids: List[Snowflake]
    entitlement_ids: List[Snowflake]
    current_period_start: str
    current_period_end: str
    status: SubscriptionStatus
    canceled_at: Optional[str]
    renewal_sku_ids: Optional[List[Snowflake]]
