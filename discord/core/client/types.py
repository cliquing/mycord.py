from typing import List, Literal, Optional, TypedDict
from typing_extensions import NotRequired, Required



from ..guild.channel import ChannelType, StageInstance, VoiceChannelEffect
from ..interaction.interactions import Interaction
from ..guild.invite import InviteTargetType
from ..emoji import Emoji, PartialEmoji
from ..guild.member import MemberWithUser
from ...utils.snowflake import Snowflake


from ..guild import Guild, UnavailableGuild
from ..user import User, AvatarDecorationData


class TypingStartEvent(TypedDict):
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int
    guild_id: NotRequired[Snowflake]
    member: NotRequired[MemberWithUser]