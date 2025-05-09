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

from typing import List, Optional, TypedDict
from ...client.activity.types import ActivityPayload
from ....utils.snowflake import Snowflake
from ...user import UserPayload


class WidgetChannelPayload(TypedDict):
    id: Snowflake
    name: str
    position: int


class WidgetMemberPayload(UserPayload, total=False):
    nick: str
    game: ActivityPayload
    status: str
    avatar_url: str
    deaf: bool
    self_deaf: bool
    mute: bool
    self_mute: bool
    suppress: bool


class WidgetPayload(TypedDict):
    id: Snowflake
    name: str
    instant_invite: Optional[str]
    channels: List[WidgetChannelPayload]
    members: List[WidgetMemberPayload]
    presence_count: int


class WidgetSettingsPayload(TypedDict):
    enabled: bool
    channel_id: Optional[Snowflake]


class EditWidgetSettingsPayload(TypedDict, total=False):
    enabled: bool
    channel_id: Optional[Snowflake]
