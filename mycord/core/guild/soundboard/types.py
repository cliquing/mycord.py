
from typing import TypedDict, Optional, Union
from typing_extensions import NotRequired

from ....utils.snowflake import Snowflake
from ...user.types import UserPayload


class BaseSoundboardSoundPayload(TypedDict):
    sound_id: Union[Snowflake, str]  # basic string number when it's a default sound
    volume: float


class SoundboardSoundPayload(BaseSoundboardSoundPayload):
    name: str
    emoji_name: Optional[str]
    emoji_id: Optional[Snowflake]
    user_id: NotRequired[Snowflake]
    available: bool
    guild_id: NotRequired[Snowflake]
    user: NotRequired[UserPayload]


class SoundboardDefaultSoundPayload(BaseSoundboardSoundPayload):
    name: str
    emoji_name: str
