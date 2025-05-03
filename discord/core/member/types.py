

from typing import List, Optional, TypedDict, Union
from ..user import User, AvatarDecorationData
from typing_extensions import NotRequired


Snowflake = Union[str, int]
SnowflakeList = List[Snowflake]

class Nickname(TypedDict):
    nick: str


class PartialMember(TypedDict):
    roles: SnowflakeList
    joined_at: str
    deaf: bool
    mute: bool
    flags: int


class Member(PartialMember, total=False):
    avatar: str
    user: User
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str
    banner: NotRequired[Optional[str]]
    avatar_decoration_data: NotRequired[AvatarDecorationData]


class _OptionalMemberWithUser(PartialMember, total=False):
    avatar: str
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str
    avatar_decoration_data: NotRequired[AvatarDecorationData]


class MemberWithUser(_OptionalMemberWithUser):
    user: User


class UserWithMember(User, total=False):
    member: _OptionalMemberWithUser
