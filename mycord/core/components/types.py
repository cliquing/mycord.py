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

from typing import List, Literal, TypedDict, Union
from typing_extensions import NotRequired

from ...core.emoji.types import PartialEmojiPayload
from ...core.guild.channel.types import ChannelTypes

ComponentType = Literal[1, 2, 3, 4]
ButtonStyle = Literal[1, 2, 3, 4, 5, 6]
TextStyle = Literal[1, 2]
DefaultValueType = Literal['user', 'role', 'channel']


class ActionRowPayload(TypedDict):
    type: Literal[1]
    components: List[ActionRowChildComponent]


class ButtonComponentPayload(TypedDict):
    type: Literal[2]
    style: ButtonStyle
    custom_id: NotRequired[str]
    url: NotRequired[str]
    disabled: NotRequired[bool]
    emoji: NotRequired[PartialEmojiPayload]
    label: NotRequired[str]
    sku_id: NotRequired[str]


class SelectOptionPayload(TypedDict):
    label: str
    value: str
    default: bool
    description: NotRequired[str]
    emoji: NotRequired[PartialEmojiPayload]


class SelectComponentPayload(TypedDict):
    custom_id: str
    placeholder: NotRequired[str]
    min_values: NotRequired[int]
    max_values: NotRequired[int]
    disabled: NotRequired[bool]


class SelectDefaultValues(TypedDict):
    id: int
    type: DefaultValueType


class StringSelectComponent(SelectComponentPayload):
    type: Literal[3]
    options: NotRequired[List[SelectOptionPayload]]


class UserSelectComponent(SelectComponentPayload):
    type: Literal[5]
    default_values: NotRequired[List[SelectDefaultValues]]


class RoleSelectComponent(SelectComponentPayload):
    type: Literal[6]
    default_values: NotRequired[List[SelectDefaultValues]]


class MentionableSelectComponent(SelectComponentPayload):
    type: Literal[7]
    default_values: NotRequired[List[SelectDefaultValues]]


class ChannelSelectComponent(SelectComponentPayload):
    type: Literal[8]
    channel_types: NotRequired[List[ChannelTypes]]
    default_values: NotRequired[List[SelectDefaultValues]]


class TextInputPayload(TypedDict):
    type: Literal[4]
    custom_id: str
    style: TextStyle
    label: str
    placeholder: NotRequired[str]
    value: NotRequired[str]
    required: NotRequired[bool]
    min_length: NotRequired[int]
    max_length: NotRequired[int]


class SelectMenuPayload(SelectComponentPayload):
    type: Literal[3, 5, 6, 7, 8]
    options: NotRequired[List[SelectOptionPayload]]
    channel_types: NotRequired[List[ChannelTypes]]
    default_values: NotRequired[List[SelectDefaultValues]]


ActionRowChildComponent = Union[ButtonComponentPayload, SelectMenuPayload, TextInputPayload]
ComponentPayload = Union[ActionRowPayload, ActionRowChildComponent]
