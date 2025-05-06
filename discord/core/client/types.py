from typing import Literal, TypedDict
from typing_extensions import NotRequired



from ..guild.member import MemberWithUser
from ...utils.snowflake import Snowflake




class TypingStartEvent(TypedDict):
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int
    guild_id: NotRequired[Snowflake]
    member: NotRequired[MemberWithUser]


StatusTypes = Literal['idle', 'dnd', 'online', 'offline']
class ClientStatusPayload(TypedDict, total=False):
    desktop: StatusTypes
    mobile: StatusTypes
    web: StatusTypes

