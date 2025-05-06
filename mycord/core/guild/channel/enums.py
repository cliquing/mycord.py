from ....utils.enums import Enum


class ChannelType(Enum):
    text = 0
    private = 1
    voice = 2
    group = 3
    category = 4
    news = 5
    news_thread = 10
    public_thread = 11
    private_thread = 12
    stage_voice = 13
    forum = 15
    media = 16

    def __str__(self) -> str:
        return self.name
    
class VideoQualityMode(Enum):
    auto = 1
    full = 2

    def __int__(self) -> int:
        return self.value

class EventStatus(Enum):
    scheduled = 1
    active = 2
    completed = 3
    canceled = 4

    ended = 3
    cancelled = 4


class ForumLayoutType(Enum):
    not_set = 0
    list_view = 1
    gallery_view = 2


class ForumOrderType(Enum):
    latest_activity = 0
    creation_date = 1


class VoiceChannelEffectAnimationType(Enum):
    premium = 0
    basic = 1

