"""
Discord API Wrapper
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the Discord API.

:copyright: (c) 2015-present Rapptz
:license: MIT, see LICENSE for more details.

"""

__title__ = 'discord'
__author__ = 'Rapptz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-present Rapptz'
__version__ = '2.6.0a'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from .other import opus as opus

from .core.client.client import *
from .other.appinfo.appinfo import *
from .core.user.user import *
from .core.emoji.emoji import *
from .core.emoji.partial_emoji import *
from .core.activity.activity import *
from .channel import *
from .core.guild.guild import *
from .flags import *
from .core.member.member import *
from .core.message.message import *
from .entity.asset import *
from .errors import *
from .entity.permissions import *
from .core.role import *
from .entity.file import *
from .entity.colour import *
from .other.integration.integrations import *
from .core.invite.invite import *
from .other.template.template import *
from .other.welcome_screen.welcome_screen import *
from .other.sku.sku import *
from .other.widget.widget import *
from .object import *
from .core.reaction.reaction import *
from . import (
    utils as utils,
    abc as abc,
    ui as ui,
    app_commands as app_commands,
)
from .enums import *
from .core.embeds.embeds import *
from .core.message.mentions import *
from .shard import *
from .player import *
from .core.webhook import *
from .core.client.voice import *
from .other.audit_logs.audit_logs import *
from .raw_models import *
from .team import *
from .other.sticker.sticker import *
from .stage_instance import *
from .other.scheduled_event.scheduled_event import *
from .core.interaction.interactions import *
from .components import *
from .other.threads.threads import *
from .other.automod.automod import *
from .other.poll.poll import *
from .other.soundboard.soundboard import *
from .other.subscription.subscription import *
from .presences import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=2, minor=6, micro=0, releaselevel='alpha', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

# This is a backwards compatibility hack and should be removed in v3
# Essentially forcing the exception to have different base classes
# In the future, this should only inherit from ClientException
if len(MissingApplicationID.__bases__) == 1:
    MissingApplicationID.__bases__ = (app_commands.AppCommandError, ClientException)

del logging, NamedTuple, Literal, VersionInfo
