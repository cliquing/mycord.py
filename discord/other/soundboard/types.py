
from typing import TypedDict, Optional, Union
from typing_extensions import NotRequired

from .snowflake import Snowflake
from .user import User


class BaseSoundboardSound(TypedDict):
    sound_id: Union[Snowflake, str]  # basic string number when it's a default sound
    volume: float


class SoundboardSound(BaseSoundboardSound):
    name: str
    emoji_name: Optional[str]
    emoji_id: Optional[Snowflake]
    user_id: NotRequired[Snowflake]
    available: bool
    guild_id: NotRequired[Snowflake]
    user: NotRequired[User]


class SoundboardDefaultSound(BaseSoundboardSound):
    name: str
    emoji_name: str
