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

from typing import Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired, Required

from ....utils.snowflake import Snowflake
from ...user import UserPayload


class IntegrationApplicationPayload(TypedDict):
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    summary: str
    bot: NotRequired[UserPayload]


class IntegrationAccountPayload(TypedDict):
    id: str
    name: str


IntegrationExpireBehavior = Literal[0, 1]


class PartialIntegrationPayload(TypedDict):
    id: Snowflake
    name: str
    type: IntegrationTypes
    account: IntegrationAccountPayload
    application_id: Snowflake


IntegrationTypes = Literal['twitch', 'youtube', 'discord', 'guild_subscription']


class BaseIntegrationPayload(PartialIntegrationPayload):
    enabled: bool
    syncing: bool
    synced_at: str
    user: UserPayload
    expire_behavior: IntegrationExpireBehavior
    expire_grace_period: int


class StreamIntegrationPayload(BaseIntegrationPayload):
    role_id: Optional[Snowflake]
    enable_emoticons: bool
    subscriber_count: int
    revoked: bool


class BotIntegrationPayload(BaseIntegrationPayload):
    application: IntegrationApplicationPayload


IntegrationPayload = Union[BaseIntegrationPayload, StreamIntegrationPayload, BotIntegrationPayload]


class _IntegrationEvent(BaseIntegrationPayload, total=False):
    guild_id: Required[Snowflake]
    role_id: Optional[Snowflake]
    enable_emoticons: bool
    subscriber_count: int
    revoked: bool
    application: IntegrationApplicationPayload


IntegrationCreateEvent = IntegrationUpdateEvent = _IntegrationEvent


class IntegrationDeleteEvent(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    application_id: NotRequired[Snowflake]



