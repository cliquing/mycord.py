

from typing import List, Optional, TypedDict
from ...user.types import UserPayload, AvatarDecorationData
from typing_extensions import NotRequired

from ....utils.snowflake import Snowflake, SnowflakeList


class NicknamePayload(TypedDict):
    nick: str


class PartialMemberPayload(TypedDict):
    roles: SnowflakeList
    joined_at: str
    deaf: bool
    mute: bool
    flags: int


class MemberPayload(PartialMemberPayload, total=False):
    avatar: str
    user: UserPayload
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str
    banner: NotRequired[Optional[str]]
    avatar_decoration_data: NotRequired[AvatarDecorationData]


class _OptionalMemberWithUser(PartialMemberPayload, total=False):
    avatar: str
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str
    avatar_decoration_data: NotRequired[AvatarDecorationData]


class MemberWithUser(_OptionalMemberWithUser):
    user: UserPayload


class UserWithMember(UserPayload, total=False):
    member: _OptionalMemberWithUser



class GuildMemberAddEvent(MemberWithUser):
    guild_id: Snowflake


class GuildMemberRemoveEvent(TypedDict):
    guild_id: Snowflake
    user: UserPayload


class GuildMemberUpdateEvent(TypedDict):
    guild_id: Snowflake
    roles: List[Snowflake]
    user: UserPayload
    avatar: Optional[str]
    joined_at: Optional[str]
    flags: int
    nick: NotRequired[str]
    premium_since: NotRequired[Optional[str]]
    deaf: NotRequired[bool]
    mute: NotRequired[bool]
    pending: NotRequired[bool]
    communication_disabled_until: NotRequired[str]
    avatar_decoration_data: NotRequired[AvatarDecorationData]