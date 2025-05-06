from typing import Literal, Optional, TypedDict
from typing_extensions import NotRequired
from ...utils.snowflake import Snowflake

__all__ = (
    "AvatarDecorationData",
    "PremiumType",
    "PartialUserPayload",
    "UserPayload",
    "UserUpdateEvent",
)

class AvatarDecorationData(TypedDict):
    asset: str
    sku_id: Snowflake


class PartialUserPayload(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    global_name: Optional[str]
    avatar_decoration_data: NotRequired[AvatarDecorationData]


PremiumType = Literal[0, 1, 2, 3]


class UserPayload(PartialUserPayload, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    locale: str
    verified: bool
    email: Optional[str]
    flags: int
    premium_type: PremiumType
    public_flags: int


UserUpdateEvent = UserPayload

