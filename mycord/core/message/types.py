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

from __future__ import annotations

from typing import List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired, Required

from ...utils.snowflake import Snowflake, SnowflakeList
from ..guild.member.types import MemberPayload, UserWithMember, MemberWithUser
from ..user import User
from ..emoji import PartialEmojiPayload
from .embeds.types import EmbedPayload
from ..guild.channel import ChannelTypes
from ..components.types import ComponentPayload
from ..interaction.types import MessageInteractionPayload, MessageInteractionMetadata
from ..guild.sticker.types import StickerItemPayload
from ..guild.threads import ThreadPayload
from .poll.types import PollPayload



class PartialMessagePayload(TypedDict):
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class ChannelMention(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    type: ChannelTypes
    name: str


class ReactionCountDetails(TypedDict):
    burst: int
    normal: int


ReactionTypes = Literal[0, 1]

class ReactionPayload(TypedDict):
    count: int
    me: bool
    emoji: PartialEmojiPayload
    me_burst: bool
    count_details: ReactionCountDetails
    burst_colors: List[str]




MessageActivityType = Literal[1, 2, 3, 5]


class MessageActivity(TypedDict):
    type: MessageActivityType
    party_id: str


class MessageApplication(TypedDict):
    id: Snowflake
    description: str
    icon: Optional[str]
    name: str
    cover_image: NotRequired[str]


MessageReferenceType = Literal[0, 1]


class MessageReference(TypedDict, total=False):
    type: MessageReferenceType
    message_id: Snowflake
    channel_id: Required[Snowflake]
    guild_id: Snowflake
    fail_if_not_exists: bool


class RoleSubscriptionData(TypedDict):
    role_subscription_listing_id: Snowflake
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool


PurchaseNotificationResponseType = Literal[0]


class GuildProductPurchase(TypedDict):
    listing_id: Snowflake
    product_name: str


class PurchaseNotificationResponse(TypedDict):
    type: PurchaseNotificationResponseType
    guild_product_purchase: Optional[GuildProductPurchase]


class CallMessage(TypedDict):
    participants: SnowflakeList
    ended_timestamp: NotRequired[Optional[str]]


MessageTypes = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 36, 37, 38, 39, 44, 46, ]

class AttachmentPayload(TypedDict):
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    height: NotRequired[Optional[int]]
    width: NotRequired[Optional[int]]
    description: NotRequired[str]
    content_type: NotRequired[str]
    spoiler: NotRequired[bool]
    ephemeral: NotRequired[bool]
    duration_secs: NotRequired[float]
    waveform: NotRequired[str]
    flags: NotRequired[int]

class MessageSnapshot(TypedDict):
    type: MessageTypes
    content: str
    embeds: List[EmbedPayload]
    attachments: List[AttachmentPayload]
    timestamp: str
    edited_timestamp: Optional[str]
    flags: NotRequired[int]
    mentions: List[UserWithMember]
    mention_roles: SnowflakeList
    sticker_items: NotRequired[List[StickerItemPayload]]
    components: NotRequired[List[ComponentPayload]]


class MessagePayload(PartialMessagePayload):
    id: Snowflake
    author: User
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: List[UserWithMember]
    mention_roles: SnowflakeList
    attachments: List[AttachmentPayload]
    embeds: List[EmbedPayload]
    pinned: bool
    poll: NotRequired[PollPayload]
    type: MessageTypes
    member: NotRequired[MemberPayload]
    mention_channels: NotRequired[List[ChannelMention]]
    reactions: NotRequired[List[ReactionPayload]]
    nonce: NotRequired[Union[int, str]]
    webhook_id: NotRequired[Snowflake]
    activity: NotRequired[MessageActivity]
    application: NotRequired[MessageApplication]
    application_id: NotRequired[Snowflake]
    message_reference: NotRequired[MessageReference]
    flags: NotRequired[int]
    sticker_items: NotRequired[List[StickerItemPayload]]
    referenced_message: NotRequired[Optional[MessagePayload]]
    interaction: NotRequired[MessageInteractionPayload]  # deprecated, use interaction_metadata
    interaction_metadata: NotRequired[MessageInteractionMetadata]
    components: NotRequired[List[ComponentPayload]]
    position: NotRequired[int]
    role_subscription_data: NotRequired[RoleSubscriptionData]
    thread: NotRequired[ThreadPayload]
    call: NotRequired[CallMessage]
    purchase_notification: NotRequired[PurchaseNotificationResponse]


AllowedMentionType = Literal['roles', 'users', 'everyone']


class AllowedMentionsPayload(TypedDict):
    parse: List[AllowedMentionType]
    roles: SnowflakeList
    users: SnowflakeList
    replied_user: bool





class MessageDeleteEvent(TypedDict):
    id: Snowflake
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class MessageDeleteBulkEvent(TypedDict):
    ids: List[Snowflake]
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


MessageCreateEvent = MessagePayload
MessageUpdateEvent = MessageCreateEvent


class MessageReactionAddEvent(TypedDict):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: PartialEmojiPayload
    member: NotRequired[MemberWithUser]
    guild_id: NotRequired[Snowflake]
    message_author_id: NotRequired[Snowflake]
    burst: bool
    burst_colors: NotRequired[List[str]]
    type: ReactionTypes


class MessageReactionRemoveEvent(TypedDict):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: PartialEmojiPayload
    guild_id: NotRequired[Snowflake]
    burst: bool
    type: ReactionTypes


class MessageReactionRemoveAllEvent(TypedDict):
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class MessageReactionRemoveEmojiEvent(TypedDict):
    emoji: PartialEmojiPayload
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]



