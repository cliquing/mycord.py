from typing import List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired

from ...user.types import PartialUserPayload
from ....utils.snowflake import Snowflake
from ..threads import ThreadMetadata, ThreadMemberPayload, ThreadArchiveDuration, ThreadType
from ...emoji import PartialEmojiPayload


OverwriteType = Literal[0, 1]


class PermissionOverwritePayload(TypedDict):
    id: Snowflake
    type: OverwriteType
    allow: str
    deny: str


ChannelTypeWithoutThread = Literal[0, 1, 2, 3, 4, 5, 6, 13, 15, 16]
ChannelTypes = Union[ChannelTypeWithoutThread, ThreadType]


class _BaseChannel(TypedDict):
    id: Snowflake
    name: str


class _BaseGuildChannel(_BaseChannel):
    guild_id: Snowflake
    position: int
    permission_overwrites: List[PermissionOverwritePayload]
    nsfw: bool
    parent_id: Optional[Snowflake]


class PartialChannelPayload(_BaseChannel):
    type: ChannelTypes


class _BaseTextChannel(_BaseGuildChannel, total=False):
    topic: str
    last_message_id: Optional[Snowflake]
    last_pin_timestamp: str
    rate_limit_per_user: int
    default_thread_rate_limit_per_user: int
    default_auto_archive_duration: ThreadArchiveDuration


class TextChannelPayload(_BaseTextChannel):
    type: Literal[0]


class NewsChannelPayload(_BaseTextChannel):
    type: Literal[5]




VideoQualityMode = Literal[1, 2]
class VoiceChannelPayload(_BaseTextChannel):
    type: Literal[2]
    bitrate: int
    user_limit: int
    rtc_region: NotRequired[Optional[str]]
    video_quality_mode: NotRequired[VideoQualityMode]


VoiceChannelEffectAnimationTypes = Literal[0, 1]

class VoiceChannelEffectPayload(TypedDict):
    guild_id: Snowflake
    channel_id: Snowflake
    user_id: Snowflake
    emoji: NotRequired[Optional[PartialEmojiPayload]]
    animation_type: NotRequired[VoiceChannelEffectAnimationTypes]
    animation_id: NotRequired[int]
    sound_id: NotRequired[Union[int, str]]
    sound_volume: NotRequired[float]


class CategoryChannelPayload(_BaseGuildChannel):
    type: Literal[4]


class StageChannelPayload(_BaseGuildChannel):
    type: Literal[13]
    bitrate: int
    user_limit: int
    rtc_region: NotRequired[Optional[str]]
    topic: NotRequired[str]


class ThreadChannelPayload(_BaseChannel):
    type: Literal[10, 11, 12]
    guild_id: Snowflake
    parent_id: Snowflake
    owner_id: Snowflake
    nsfw: bool
    last_message_id: Optional[Snowflake]
    rate_limit_per_user: int
    message_count: int
    member_count: int
    thread_metadata: ThreadMetadata
    member: NotRequired[ThreadMemberPayload]
    owner_id: NotRequired[Snowflake]
    rate_limit_per_user: NotRequired[int]
    last_message_id: NotRequired[Optional[Snowflake]]
    last_pin_timestamp: NotRequired[str]
    flags: NotRequired[int]
    applied_tags: NotRequired[List[Snowflake]]


class DefaultReactionPayload(TypedDict):
    emoji_id: Optional[Snowflake]
    emoji_name: Optional[str]


class ForumTagPayload(TypedDict):
    id: Snowflake
    name: str
    moderated: bool
    emoji_id: Optional[Snowflake]
    emoji_name: Optional[str]


ForumOrderTypes = Literal[0, 1]
ForumLayoutType = Literal[0, 1, 2]


class _BaseForumChannel(_BaseTextChannel):
    available_tags: List[ForumTagPayload]
    default_reaction_emoji: Optional[DefaultReactionPayload]
    default_sort_order: Optional[ForumOrderTypes]
    default_forum_layout: NotRequired[ForumLayoutType]
    flags: NotRequired[int]


class ForumChannelPayload(_BaseForumChannel):
    type: Literal[15]


class MediaChannelPayload(_BaseForumChannel):
    type: Literal[16]


GuildChannelPayload = Union[
    TextChannelPayload, NewsChannelPayload, VoiceChannelPayload, CategoryChannelPayload, StageChannelPayload, ThreadChannelPayload, ForumChannelPayload, MediaChannelPayload
]


class _BaseDMChannel(_BaseChannel):
    type: Literal[1]
    last_message_id: Optional[Snowflake]


class DMChannelPayload(_BaseDMChannel):
    recipients: List[PartialUserPayload]


class InteractionDMChannelPayload(_BaseDMChannel):
    recipients: NotRequired[List[PartialUserPayload]]


class GroupDMChannelPayload(_BaseChannel):
    type: Literal[3]
    icon: Optional[str]
    owner_id: Snowflake
    recipients: List[PartialUserPayload]

GroupChannelPayload = GroupDMChannelPayload

ChannelPayload = Union[GuildChannelPayload, DMChannelPayload, GroupDMChannelPayload]

PrivacyLevel = Literal[2]


class StageInstancePayload(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable_disabled: bool
    guild_scheduled_event_id: Optional[int]


#---

class _ChannelEvent(TypedDict):
    id: Snowflake
    type: ChannelTypes


ChannelCreateEvent = ChannelUpdateEvent = ChannelDeleteEvent = _ChannelEvent


class ChannelPinsUpdateEvent(TypedDict):
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]
    last_pin_timestamp: NotRequired[Optional[str]]


StageInstanceCreateEvent = StageInstanceUpdateEvent = StageInstanceDeleteEvent = StageInstancePayload




VoiceChannelEffectSendEvent = VoiceChannelEffectPayload