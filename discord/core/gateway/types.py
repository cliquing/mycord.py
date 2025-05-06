"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from typing import List, Literal, Optional, TypedDict
from typing_extensions import NotRequired

from ..guild.automod import AutoModerationAction, AutoModerationRuleTriggerType
from ..client.activity import PartialPresenceUpdate
from ..state.types import GuildVoiceStatePayload
from ..guild.channel import VoiceChannelEffect
from ..guild.channel.types import StageInstancePayload
from ..interaction.interactions import Interaction
from ..guild.member import MemberWithUser
from ...utils.snowflake import Snowflake

from ..appinfo import GatewayAppInfoPayload
from ..guild import UnavailableGuild
from ..user import UserPayload
from ..guild.scheduled_event import GuildScheduledEvent
from ..guild.soundboard import SoundboardSound


class SessionStartLimit(TypedDict):
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


class Gateway(TypedDict):
    url: str


class GatewayBot(Gateway):
    shards: int
    session_start_limit: SessionStartLimit


class ReadyEvent(TypedDict):
    v: int
    user: UserPayload
    guilds: List[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: List[int]  # shard_id, num_shards
    application: GatewayAppInfoPayload


ResumedEvent = Literal[None]




InteractionCreateEvent = Interaction


PresenceUpdateEvent = PartialPresenceUpdate


UserUpdateEvent = UserPayload





StageInstancePayloadCreateEvent = StageInstancePayloadUpdateEvent = StageInstancePayloadDeleteEvent = StageInstancePayload



GuildScheduledEventCreateEvent = GuildScheduledEventUpdateEvent = GuildScheduledEventDeleteEvent = GuildScheduledEvent


class _GuildScheduledEventUsersEvent(TypedDict):
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


GuildScheduledEventUserAdd = GuildScheduledEventUserRemove = _GuildScheduledEventUsersEvent

VoiceStateUpdateEvent = GuildVoiceStatePayload
VoiceChannelEffectSendEvent = VoiceChannelEffect

GuildSoundBoardSoundCreateEvent = GuildSoundBoardSoundUpdateEvent = SoundboardSound


class GuildSoundBoardSoundsUpdateEvent(TypedDict):
    guild_id: Snowflake
    soundboard_sounds: List[SoundboardSound]


class GuildSoundBoardSoundDeleteEvent(TypedDict):
    sound_id: Snowflake
    guild_id: Snowflake


class VoiceServerUpdateEvent(TypedDict):
    token: str
    guild_id: Snowflake
    endpoint: Optional[str]


class TypingStartEvent(TypedDict):
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int
    guild_id: NotRequired[Snowflake]
    member: NotRequired[MemberWithUser]


class AutoModerationActionExecution(TypedDict):
    guild_id: Snowflake
    action: AutoModerationAction
    rule_id: Snowflake
    rule_trigger_type: AutoModerationRuleTriggerType
    user_id: Snowflake
    channel_id: NotRequired[Snowflake]
    message_id: NotRequired[Snowflake]
    alert_system_message_id: NotRequired[Snowflake]
    content: str
    matched_keyword: Optional[str]
    matched_content: Optional[str]










