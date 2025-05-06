
from typing import List, Literal, Optional, TypedDict
from typing_extensions import NotRequired

from .scheduled_event import GuildScheduledEvent
from .sticker import GuildStickerPayload
from ...utils.snowflake import Snowflake
from .channel.types import GuildChannelPayload, StageInstancePayload
from ..state.types import GuildVoiceStatePayload
from .welcome_screen import WelcomeScreen
from .role import RolePayload
from .member import MemberPayload
from ..emoji import EmojiPayload
from ..user import UserPayload
from .threads import ThreadPayload
from .soundboard.types import SoundboardSoundPayload

from .member import MemberWithUser
from ..user import AvatarDecorationData
from ..client.activity import PresenceUpdateEvent, PartialPresenceUpdate
from .audit_logs import AuditLogEntryPayload


class BanPayload(TypedDict):
    reason: Optional[str]
    user: UserPayload


class UnavailableGuild(TypedDict):
    id: Snowflake
    unavailable: NotRequired[bool]


class IncidentData(TypedDict):
    invites_disabled_until: NotRequired[Optional[str]]
    dms_disabled_until: NotRequired[Optional[str]]


DefaultMessageNotificationLevel = Literal[0, 1]
ExplicitContentFilterLevel = Literal[0, 1, 2]
MFALevels = Literal[0, 1]
VerificationLevels = Literal[0, 1, 2, 3, 4]
NSFWLevels = Literal[0, 1, 2, 3]
PremiumTier = Literal[0, 1, 2, 3]
GuildFeatures = Literal[
    'ANIMATED_BANNER', 'ANIMATED_ICON', 'APPLICATION_COMMAND_PERMISSIONS_V2', 'AUTO_MODERATION','BANNER',
    'COMMUNITY', 'CREATOR_MONETIZABLE_PROVISIONAL', 'CREATOR_STORE_PAGE','DEVELOPER_SUPPORT_SERVER', 'DISCOVERABLE','FEATURABLE', 'INVITE_SPLASH', 'INVITES_DISABLED',
    'MEMBER_VERIFICATION_GATE_ENABLED', 'MONETIZATION_ENABLED', 'MORE_EMOJI','MORE_STICKERS', 'NEWS', 'PARTNERED', 'PREVIEW_ENABLED','ROLE_ICONS',
    'ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE', 'ROLE_SUBSCRIPTIONS_ENABLED', 'TICKETED_EVENTS_ENABLED', 'VANITY_URL', 'VERIFIED',
    'VIP_REGIONS', 'WELCOME_SCREEN_ENABLED', 'RAID_ALERTS_DISABLED', 'SOUNDBOARD', 'MORE_SOUNDBOARD',
]



class _BaseGuildPreview(UnavailableGuild):
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    emojis: List[EmojiPayload]
    stickers: List[GuildStickerPayload]
    features: List[GuildFeatures]
    description: Optional[str]
    incidents_data: Optional[IncidentData]


class _GuildPreviewUnique(TypedDict):
    approximate_member_count: int
    approximate_presence_count: int


class GuildPreviewPayload(_BaseGuildPreview, _GuildPreviewUnique):
    ...


class GuildPayload(_BaseGuildPreview):
    owner_id: Snowflake
    region: str
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    verification_level: VerificationLevels
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: List[RolePayload]
    mfa_level: MFALevels
    nsfw_level: NSFWLevels
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: int
    rules_channel_id: Optional[Snowflake]
    vanity_url_code: Optional[str]
    banner: Optional[str]
    premium_tier: PremiumTier
    preferred_locale: str
    public_updates_channel_id: Optional[Snowflake]
    stickers: List[GuildStickerPayload]
    stage_instances: List[StageInstancePayload]
    guild_scheduled_events: List[GuildScheduledEvent]
    icon_hash: NotRequired[Optional[str]]
    owner: NotRequired[bool]
    permissions: NotRequired[str]
    widget_enabled: NotRequired[bool]
    widget_channel_id: NotRequired[Optional[Snowflake]]
    joined_at: NotRequired[Optional[str]]
    large: NotRequired[bool]
    member_count: NotRequired[int]
    voice_states: NotRequired[List[GuildVoiceStatePayload]]
    members: NotRequired[List[MemberPayload]]
    channels: NotRequired[List[GuildChannelPayload]]
    presences: NotRequired[List[PartialPresenceUpdate]]
    threads: NotRequired[List[ThreadPayload]]
    max_presences: NotRequired[Optional[int]]
    max_members: NotRequired[int]
    premium_subscription_count: NotRequired[int]
    max_video_channel_users: NotRequired[int]
    soundboard_sounds: NotRequired[List[SoundboardSoundPayload]]


class InviteGuildPayload(GuildPayload, total=False):
    welcome_screen: WelcomeScreen


class GuildWithCounts(GuildPayload, _GuildPreviewUnique):
    ...


class GuildPrune(TypedDict):
    pruned: Optional[int]


class GuildMFALevel(TypedDict):
    level: MFALevels


class ChannelPositionUpdate(TypedDict):
    id: Snowflake
    position: Optional[int]
    lock_permissions: NotRequired[Optional[bool]]
    parent_id: NotRequired[Optional[Snowflake]]


class _RolePositionRequired(TypedDict):
    id: Snowflake


class RolePositionUpdatePayload(_RolePositionRequired, total=False):
    position: Optional[Snowflake]


class BulkBanUserResponse(TypedDict):
    banned_users: Optional[List[Snowflake]]
    failed_users: Optional[List[Snowflake]]



#---


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


class GuildEmojisUpdateEvent(TypedDict):
    guild_id: Snowflake
    emojis: List[EmojiPayload]


class GuildStickersUpdateEvent(TypedDict):
    guild_id: Snowflake
    stickers: List[GuildStickerPayload]


GuildCreateEvent = GuildUpdateEvent = GuildPayload
GuildDeleteEvent = UnavailableGuild


class _GuildBanEvent(TypedDict):
    guild_id: Snowflake
    user: UserPayload


GuildBanAddEvent = GuildBanRemoveEvent = _GuildBanEvent


class _GuildRoleEvent(TypedDict):
    guild_id: Snowflake
    role: RolePayload


class GuildRoleDeleteEvent(TypedDict):
    guild_id: Snowflake
    role_id: Snowflake


GuildRoleCreateEvent = GuildRoleUpdateEvent = _GuildRoleEvent



class GuildMembersChunkEvent(TypedDict):
    guild_id: Snowflake
    members: List[MemberWithUser]
    chunk_index: int
    chunk_count: int
    not_found: NotRequired[List[Snowflake]]
    presences: NotRequired[List[PresenceUpdateEvent]]
    nonce: NotRequired[str]


class GuildIntegrationsUpdateEvent(TypedDict):
    guild_id: Snowflake


##--

GuildScheduledEventCreateEvent = GuildScheduledEventUpdateEvent = GuildScheduledEventDeleteEvent = GuildScheduledEvent


class _GuildScheduledEventUsersEvent(TypedDict):
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


GuildScheduledEventUserAdd = GuildScheduledEventUserRemove = _GuildScheduledEventUsersEvent

VoiceStateUpdateEvent = GuildVoiceStatePayload
from .channel import VoiceChannelEffectPayload
VoiceChannelEffectSendEvent = VoiceChannelEffectPayload

GuildSoundBoardSoundCreateEvent = GuildSoundBoardSoundUpdateEvent = SoundboardSoundPayload


class GuildSoundBoardSoundsUpdateEvent(TypedDict):
    guild_id: Snowflake
    soundboard_sounds: List[SoundboardSoundPayload]


class GuildSoundBoardSoundDeleteEvent(TypedDict):
    sound_id: Snowflake
    guild_id: Snowflake


class VoiceServerUpdateEvent(TypedDict):
    token: str
    guild_id: Snowflake
    endpoint: Optional[str]




class GuildAuditLogEntryCreate(AuditLogEntryPayload):
    guild_id: Snowflake



