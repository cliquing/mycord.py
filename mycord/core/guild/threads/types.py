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

from typing import List, Literal, Optional, TypedDict
from typing_extensions import NotRequired

from ....utils.snowflake import Snowflake
from ...message import MessagePayload

ThreadType = Literal[10, 11, 12]
ThreadArchiveDuration = Literal[60, 1440, 4320, 10080]

from ..channel.types import ChannelTypes

class ThreadMemberPayload(TypedDict):
    id: Snowflake
    user_id: Snowflake
    join_timestamp: str
    flags: int


class ThreadMetadata(TypedDict):
    archived: bool
    auto_archive_duration: ThreadArchiveDuration
    archive_timestamp: str
    archiver_id: NotRequired[Snowflake]
    locked: NotRequired[bool]
    invitable: NotRequired[bool]
    create_timestamp: NotRequired[str]


class ThreadPayload(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    parent_id: Snowflake
    owner_id: Snowflake
    name: str
    type: ThreadType
    member_count: int
    message_count: int
    rate_limit_per_user: int
    thread_metadata: ThreadMetadata
    member: NotRequired[ThreadMemberPayload]
    last_message_id: NotRequired[Optional[Snowflake]]
    last_pin_timestamp: NotRequired[Optional[Snowflake]]
    newly_created: NotRequired[bool]
    flags: NotRequired[int]
    applied_tags: NotRequired[List[Snowflake]]


class ThreadPaginationPayload(TypedDict):
    threads: List[ThreadPayload]
    members: List[ThreadMemberPayload]
    has_more: bool


class ForumThreadPayload(ThreadPayload):
    message: MessagePayload



#--
class ThreadCreateEvent(ThreadPayload, total=False):
    newly_created: bool
    members: List[ThreadMemberPayload]


ThreadUpdateEvent = ThreadPayload


class ThreadDeleteEvent(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    parent_id: Snowflake
    type: ChannelTypes


class ThreadListSyncEvent(TypedDict):
    guild_id: Snowflake
    threads: List[ThreadPayload]
    members: List[ThreadMemberPayload]
    channel_ids: NotRequired[List[Snowflake]]


class ThreadMemberUpdate(ThreadMemberPayload):
    guild_id: Snowflake


class ThreadMembersUpdate(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: NotRequired[List[ThreadMemberPayload]]
    removed_member_ids: NotRequired[List[Snowflake]]



