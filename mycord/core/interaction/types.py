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

from typing import TYPE_CHECKING, Dict, List, Literal, TypedDict, Union
from typing_extensions import NotRequired

from ..guild.channel.types import ChannelTypeWithoutThread, GuildChannelPayload, InteractionDMChannelPayload, GroupDMChannelPayload
from ..guild.threads.types import ThreadMetadata
from ..client.sku import EntitlementPayload
from ..guild.threads import ThreadType
from ..guild.member import MemberPayload
from ..message import AttachmentPayload
from ..guild.role import RolePayload
from ...utils.snowflake import Snowflake
from ..user import UserPayload
from ..guild import GuildFeatures

if TYPE_CHECKING:
    from ..message import MessagePayload


InteractionTypes = Literal[1, 2, 3, 4, 5]
InteractionResponseType = Literal[
    1,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
]
InteractionContextType = Literal[0, 1, 2]
InteractionInstallationType = Literal[0, 1]


class _BasePartialChannel(TypedDict):
    id: Snowflake
    name: str
    permissions: str


class PartialInteractionChannelPayload(_BasePartialChannel):
    type: ChannelTypeWithoutThread


class PartialThreadPayload(_BasePartialChannel):
    type: ThreadType
    thread_metadata: ThreadMetadata
    parent_id: Snowflake


class ResolvedData(TypedDict, total=False):
    users: Dict[str, UserPayload]
    members: Dict[str, MemberPayload]
    roles: Dict[str, RolePayload]
    channels: Dict[str, Union[PartialInteractionChannelPayload, PartialThreadPayload]]
    messages: Dict[str, MessagePayload]
    attachments: Dict[str, AttachmentPayload]


class PartialInteractionGuild(TypedDict):
    id: Snowflake
    locale: str
    features: List[GuildFeatures]


class _BaseApplicationCommandInteractionDataOption(TypedDict):
    name: str


class _CommandGroupApplicationCommandInteractionDataOption(_BaseApplicationCommandInteractionDataOption):
    type: Literal[1, 2]
    options: List[ApplicationCommandInteractionDataOption]


class _BaseValueApplicationCommandInteractionDataOption(_BaseApplicationCommandInteractionDataOption, total=False):
    focused: bool


class _StringValueApplicationCommandInteractionDataOption(_BaseValueApplicationCommandInteractionDataOption):
    type: Literal[3]
    value: str


class _IntegerValueApplicationCommandInteractionDataOption(_BaseValueApplicationCommandInteractionDataOption):
    type: Literal[4]
    value: int


class _BooleanValueApplicationCommandInteractionDataOption(_BaseValueApplicationCommandInteractionDataOption):
    type: Literal[5]
    value: bool


class _SnowflakeValueApplicationCommandInteractionDataOption(_BaseValueApplicationCommandInteractionDataOption):
    type: Literal[6, 7, 8, 9, 11]
    value: Snowflake


class _NumberValueApplicationCommandInteractionDataOption(_BaseValueApplicationCommandInteractionDataOption):
    type: Literal[10]
    value: float


_ValueApplicationCommandInteractionDataOption = Union[_StringValueApplicationCommandInteractionDataOption, _IntegerValueApplicationCommandInteractionDataOption, _BooleanValueApplicationCommandInteractionDataOption, _SnowflakeValueApplicationCommandInteractionDataOption, _NumberValueApplicationCommandInteractionDataOption,
]


ApplicationCommandInteractionDataOption = Union[
    _CommandGroupApplicationCommandInteractionDataOption,
    _ValueApplicationCommandInteractionDataOption,
]


class _BaseApplicationCommandInteractionData(TypedDict):
    id: Snowflake
    name: str
    resolved: NotRequired[ResolvedData]
    guild_id: NotRequired[Snowflake]


class ChatInputApplicationCommandInteractionData(_BaseApplicationCommandInteractionData, total=False):
    type: Literal[1]
    options: List[ApplicationCommandInteractionDataOption]


class _BaseNonChatInputApplicationCommandInteractionData(_BaseApplicationCommandInteractionData):
    target_id: Snowflake


class UserApplicationCommandInteractionData(_BaseNonChatInputApplicationCommandInteractionData):
    type: Literal[2]


class MessageApplicationCommandInteractionData(_BaseNonChatInputApplicationCommandInteractionData):
    type: Literal[3]


ApplicationCommandInteractionData = Union[ChatInputApplicationCommandInteractionData,UserApplicationCommandInteractionData, MessageApplicationCommandInteractionData,
]


class _BaseMessageComponentInteractionData(TypedDict):
    custom_id: str


class ButtonMessageComponentInteractionData(_BaseMessageComponentInteractionData):
    component_type: Literal[2]


class SelectMessageComponentInteractionData(_BaseMessageComponentInteractionData):
    component_type: Literal[3, 5, 6, 7, 8]
    values: List[str]
    resolved: NotRequired[ResolvedData]


MessageComponentInteractionData = Union[ButtonMessageComponentInteractionData, SelectMessageComponentInteractionData]


class ModalSubmitTextInputInteractionData(TypedDict):
    type: Literal[4]
    custom_id: str
    value: str


ModalSubmitComponentItemInteractionData = ModalSubmitTextInputInteractionData


class ModalSubmitActionRowInteractionData(TypedDict):
    type: Literal[1]
    components: List[ModalSubmitComponentItemInteractionData]


ModalSubmitComponentInteractionData = Union[ModalSubmitActionRowInteractionData, ModalSubmitComponentItemInteractionData]


class ModalSubmitInteractionData(TypedDict):
    custom_id: str
    components: List[ModalSubmitComponentInteractionData]


InteractionData = Union[
    ApplicationCommandInteractionData,
    MessageComponentInteractionData,
    ModalSubmitInteractionData,
]


class _BaseInteraction(TypedDict):
    id: Snowflake
    application_id: Snowflake
    token: str
    version: Literal[1]
    guild_id: NotRequired[Snowflake]
    guild: NotRequired[PartialInteractionGuild]
    channel_id: NotRequired[Snowflake]
    channel: Union[GuildChannelPayload, InteractionDMChannelPayload, GroupDMChannelPayload]
    app_permissions: NotRequired[str]
    locale: NotRequired[str]
    guild_locale: NotRequired[str]
    entitlement_sku_ids: NotRequired[List[Snowflake]]
    entitlements: NotRequired[List[EntitlementPayload]]
    authorizing_integration_owners: Dict[Literal['0', '1'], Snowflake]
    context: NotRequired[InteractionContextType]


class PingInteraction(_BaseInteraction):
    type: Literal[1]


class ApplicationCommandInteraction(_BaseInteraction):
    type: Literal[2, 4]
    data: ApplicationCommandInteractionData


class MessageComponentInteraction(_BaseInteraction):
    type: Literal[3]
    data: MessageComponentInteractionData


class ModalSubmitInteraction(_BaseInteraction):
    type: Literal[5]
    data: ModalSubmitInteractionData




class MessageInteractionPayload(TypedDict):
    id: Snowflake
    type: InteractionTypes
    name: str
    user: UserPayload
    member: NotRequired[MemberPayload]


class _MessageInteractionMetadata(TypedDict):
    id: Snowflake
    user: UserPayload
    authorizing_integration_owners: Dict[Literal['0', '1'], Snowflake]
    original_response_message_id: NotRequired[Snowflake]


class _ApplicationCommandMessageInteractionMetadata(_MessageInteractionMetadata):
    type: Literal[2]
    # command_type: Literal[1, 2, 3, 4]


class UserApplicationCommandMessageInteractionMetadata(_ApplicationCommandMessageInteractionMetadata):
    # command_type: Literal[2]
    target_user: UserPayload


class MessageApplicationCommandMessageInteractionMetadata(_ApplicationCommandMessageInteractionMetadata):
    # command_type: Literal[3]
    target_message_id: Snowflake


ApplicationCommandMessageInteractionMetadata = Union[
    _ApplicationCommandMessageInteractionMetadata,
    UserApplicationCommandMessageInteractionMetadata,
    MessageApplicationCommandMessageInteractionMetadata,
]


class MessageComponentMessageInteractionMetadata(_MessageInteractionMetadata):
    type: Literal[3]
    interacted_message_id: Snowflake


class ModalSubmitMessageInteractionMetadata(_MessageInteractionMetadata):
    type: Literal[5]
    triggering_interaction_metadata: Union[
        ApplicationCommandMessageInteractionMetadata, MessageComponentMessageInteractionMetadata
    ]


MessageInteractionMetadata = Union[
    ApplicationCommandMessageInteractionMetadata,
    MessageComponentMessageInteractionMetadata,
    ModalSubmitMessageInteractionMetadata,
]


class InteractionCallbackResponsePayload(TypedDict):
    id: Snowflake
    type: InteractionTypes
    activity_instance_id: NotRequired[str]
    response_message_id: NotRequired[Snowflake]
    response_message_loading: NotRequired[bool]
    response_message_ephemeral: NotRequired[bool]


class InteractionCallbackActivityPayload(TypedDict):
    id: str


class InteractionCallbackResource(TypedDict):
    type: InteractionResponseType
    activity_instance: NotRequired[InteractionCallbackActivityPayload]
    message: NotRequired[MessagePayload]


class InteractionCallbackPayload(TypedDict):
    interaction: InteractionCallbackResponsePayload
    resource: NotRequired[InteractionCallbackResource]


InteractionPayload = Union[PingInteraction, ApplicationCommandInteraction, MessageComponentInteraction, ModalSubmitInteraction]

InteractionCreateEvent = InteractionPayload