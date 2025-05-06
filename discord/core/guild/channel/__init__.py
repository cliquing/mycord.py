from .text import TextChannel
from .voice import VoiceChannel, VocalGuildChannel, StageChannel, VoiceChannelEffect, VoiceChannelEffectAnimation
from .types import *
from .enums import ChannelType, VideoQualityMode, ForumLayoutType, ForumOrderType, VoiceChannelEffectAnimationType, EventStatus
from .flags import ChannelFlags, SystemChannelFlags
from .other import DMChannel, CategoryChannel, ForumChannel, GroupChannel, PartialMessageable, ForumTag

from ..threads import Thread
from .stage_instance import StageInstance

from ....utils.enums import try_enum

def _guild_channel_factory(channel_type: int):
    value = try_enum(ChannelType, channel_type)
    if value is ChannelType.text:
        return TextChannel, value
    elif value is ChannelType.voice:
        return VoiceChannel, value
    elif value is ChannelType.category:
        return CategoryChannel, value
    elif value is ChannelType.news:
        return TextChannel, value
    elif value is ChannelType.stage_voice:
        return StageChannel, value
    elif value is ChannelType.forum:
        return ForumChannel, value
    elif value is ChannelType.media:
        return ForumChannel, value
    else:
        return None, value


def _channel_factory(channel_type: int):
    cls, value = _guild_channel_factory(channel_type)
    if value is ChannelType.private:
        return DMChannel, value
    elif value is ChannelType.group:
        return GroupChannel, value
    else:
        return cls, value


def _threaded_channel_factory(channel_type: int):
    cls, value = _channel_factory(channel_type)
    if value in (ChannelType.private_thread, ChannelType.public_thread, ChannelType.news_thread):
        return Thread, value
    return cls, value


def _threaded_guild_channel_factory(channel_type: int):
    cls, value = _guild_channel_factory(channel_type)
    if value in (ChannelType.private_thread, ChannelType.public_thread, ChannelType.news_thread):
        return Thread, value
    return cls, value

__all__ = (
    'ChannelType',
    'VideoQualityMode',
    'ForumLayoutType',
    'ForumOrderType',
    'VoiceChannelEffectAnimationType',
    'EventStatus',
    'ChannelFlags',
    'SystemChannelFlags',
    'TextChannel',
    'VoiceChannel',
    'VocalGuildChannel',
    'StageChannel',
    'VoiceChannelEffect',
    'VoiceChannelEffectAnimation',
    'DMChannel',
    'CategoryChannel',
    'ForumChannel',
    'PartialMessageable',
    'GroupChannel',
    'PartialMessageable',
    'ForumTag',
    'Thread',
    'StageInstance',

)