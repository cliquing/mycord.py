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

import types
from collections import namedtuple
from typing import Any, ClassVar, Dict, List, Optional, TYPE_CHECKING, Tuple, Type, TypeVar, Iterator, Mapping

__all__ = (
    'Enum',
    'ChannelType',
    'MessageType',
    'SpeakingState',
    'VerificationLevel',
    'ContentFilter',
    'Status',
    'DefaultAvatar',
    'AuditLogAction',
    'AuditLogActionCategory',
    'UserFlags',
    'ActivityType',
    'NotificationLevel',
    'TeamMembershipState',
    'TeamMemberRole',
    'WebhookType',
    'ExpireBehaviour',
    'ExpireBehavior',
    'StickerType',
    'StickerFormatType',
    'InviteTarget',
    'VideoQualityMode',
    'ComponentType',
    'ButtonStyle',
    'TextStyle',
    'PrivacyLevel',
    'InteractionType',
    'InteractionResponseType',
    'NSFWLevel',
    'MFALevel',
    'Locale',
    'EntityType',
    'EventStatus',
    'AppCommandType',
    'AppCommandOptionType',
    'AppCommandPermissionType',
    'AutoModRuleTriggerType',
    'AutoModRuleEventType',
    'AutoModRuleActionType',
    'ForumLayoutType',
    'ForumOrderType',
    'SelectDefaultValueType',
    'SKUType',
    'EntitlementType',
    'EntitlementOwnerType',
    'PollLayoutType',
    'VoiceChannelEffectAnimationType',
    'SubscriptionStatus',
    'MessageReferenceType',
)


def _create_value_cls(name: str, comparable: bool):
    # All the type ignores here are due to the type checker being unable to recognise
    # Runtime type creation without exploding.
    cls = namedtuple('_EnumValue_' + name, 'name value')
    cls.__repr__ = lambda self: f'<{name}.{self.name}: {self.value!r}>'
    cls.__str__ = lambda self: f'{name}.{self.name}'
    if comparable:
        cls.__le__ = lambda self, other: isinstance(other, self.__class__) and self.value <= other.value
        cls.__ge__ = lambda self, other: isinstance(other, self.__class__) and self.value >= other.value
        cls.__lt__ = lambda self, other: isinstance(other, self.__class__) and self.value < other.value
        cls.__gt__ = lambda self, other: isinstance(other, self.__class__) and self.value > other.value
    return cls


def _is_descriptor(obj):
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


class EnumMeta(type):
    if TYPE_CHECKING:
        __name__: ClassVar[str]
        _enum_member_names_: ClassVar[List[str]]
        _enum_member_map_: ClassVar[Dict[str, Any]]
        _enum_value_map_: ClassVar[Dict[Any, Any]]

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any],
        *,
        comparable: bool = False,
    ) -> EnumMeta:
        value_mapping = {}
        member_mapping = {}
        member_names = []

        value_cls = _create_value_cls(name, comparable)
        for key, value in list(attrs.items()):
            is_descriptor = _is_descriptor(value)
            if key[0] == '_' and not is_descriptor:
                continue

            # Special case classmethod to just pass through
            if isinstance(value, classmethod):
                continue

            if is_descriptor:
                setattr(value_cls, key, value)
                del attrs[key]
                continue

            try:
                new_value = value_mapping[value]
            except KeyError:
                new_value = value_cls(name=key, value=value)
                value_mapping[value] = new_value
                member_names.append(key)

            member_mapping[key] = new_value
            attrs[key] = new_value

        attrs['_enum_value_map_'] = value_mapping
        attrs['_enum_member_map_'] = member_mapping
        attrs['_enum_member_names_'] = member_names
        attrs['_enum_value_cls_'] = value_cls
        actual_cls = super().__new__(cls, name, bases, attrs)
        value_cls._actual_enum_cls_ = actual_cls  # type: ignore # Runtime attribute isn't understood
        return actual_cls

    def __iter__(cls) -> Iterator[Any]:
        return (cls._enum_member_map_[name] for name in cls._enum_member_names_)

    def __reversed__(cls) -> Iterator[Any]:
        return (cls._enum_member_map_[name] for name in reversed(cls._enum_member_names_))

    def __len__(cls) -> int:
        return len(cls._enum_member_names_)

    def __repr__(cls) -> str:
        return f'<enum {cls.__name__}>'

    @property
    def __members__(cls) -> Mapping[str, Any]:
        return types.MappingProxyType(cls._enum_member_map_)

    def __call__(cls, value: str) -> Any:
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            raise ValueError(f"{value!r} is not a valid {cls.__name__}")

    def __getitem__(cls, key: str) -> Any:
        return cls._enum_member_map_[key]

    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError('Enums are immutable.')

    def __delattr__(cls, attr: str) -> None:
        raise TypeError('Enums are immutable')

    def __instancecheck__(self, instance: Any) -> bool:
        # isinstance(x, Y)
        # -> __instancecheck__(Y, x)
        try:
            return instance._actual_enum_cls_ is self
        except AttributeError:
            return False


if TYPE_CHECKING:
    from enum import Enum
else:

    class Enum(metaclass=EnumMeta):
        @classmethod
        def try_value(cls, value):
            try:
                return cls._enum_value_map_[value]
            except (KeyError, TypeError):
                return value






class SpeakingState(Enum):
    none = 0
    voice = 1
    soundshare = 2
    priority = 4

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value


class VerificationLevel(Enum, comparable=True):
    none = 0
    low = 1
    medium = 2
    high = 3
    highest = 4

    def __str__(self) -> str:
        return self.name


class ContentFilter(Enum, comparable=True):
    disabled = 0
    no_role = 1
    all_members = 2

    def __str__(self) -> str:
        return self.name


class Status(Enum):
    online = 'online'
    offline = 'offline'
    idle = 'idle'
    dnd = 'dnd'
    do_not_disturb = 'dnd'
    invisible = 'invisible'

    def __str__(self) -> str:
        return self.value













class ExpireBehaviour(Enum):
    remove_role = 0
    kick = 1


ExpireBehavior = ExpireBehaviour








class ComponentType(Enum):
    action_row = 1
    button = 2
    select = 3
    string_select = 3
    text_input = 4
    user_select = 5
    role_select = 6
    mentionable_select = 7
    channel_select = 8

    def __int__(self) -> int:
        return self.value


class ButtonStyle(Enum):
    primary = 1
    secondary = 2
    success = 3
    danger = 4
    link = 5
    premium = 6

    # Aliases
    blurple = 1
    grey = 2
    gray = 2
    green = 3
    red = 4
    url = 5

    def __int__(self) -> int:
        return self.value


class TextStyle(Enum):
    short = 1
    paragraph = 2

    # Aliases
    long = 2

    def __int__(self) -> int:
        return self.value




class Locale(Enum):
    american_english = 'en-US'
    british_english = 'en-GB'
    bulgarian = 'bg'
    chinese = 'zh-CN'
    taiwan_chinese = 'zh-TW'
    croatian = 'hr'
    czech = 'cs'
    indonesian = 'id'
    danish = 'da'
    dutch = 'nl'
    finnish = 'fi'
    french = 'fr'
    german = 'de'
    greek = 'el'
    hindi = 'hi'
    hungarian = 'hu'
    italian = 'it'
    japanese = 'ja'
    korean = 'ko'
    latin_american_spanish = 'es-419'
    lithuanian = 'lt'
    norwegian = 'no'
    polish = 'pl'
    brazil_portuguese = 'pt-BR'
    romanian = 'ro'
    russian = 'ru'
    spain_spanish = 'es-ES'
    swedish = 'sv-SE'
    thai = 'th'
    turkish = 'tr'
    ukrainian = 'uk'
    vietnamese = 'vi'

    def __str__(self) -> str:
        return self.value


E = TypeVar('E', bound='Enum')


class EntityType(Enum):
    stage_instance = 1
    voice = 2
    external = 3




class SelectDefaultValueType(Enum):
    user = 'user'
    role = 'role'
    channel = 'channel'







class PollLayoutType(Enum):
    default = 1











def create_unknown_value(cls: Type[E], val: Any) -> E:
    value_cls = cls._enum_value_cls_  # type: ignore # This is narrowed below
    name = f'unknown_{val}'
    return value_cls(name=name, value=val)


def try_enum(cls: Type[E], val: Any) -> E:
    """A function that tries to turn the value into enum ``cls``.

    If it fails it returns a proxy invalid value instead.
    """

    try:
        return cls._enum_value_map_[val]  # type: ignore # All errors are caught below
    except (KeyError, TypeError, AttributeError):
        return create_unknown_value(cls, val)
