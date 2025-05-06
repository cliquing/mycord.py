from typing import Dict, Optional

from ....utils.enums import Enum

class AuditLogActionCategory(Enum):
    create = 1
    delete = 2
    update = 3


class AuditLogAction(Enum):
    # fmt: off
    guild_update                                      = 1
    channel_create                                    = 10
    channel_update                                    = 11
    channel_delete                                    = 12
    overwrite_create                                  = 13
    overwrite_update                                  = 14
    overwrite_delete                                  = 15
    kick                                              = 20
    member_prune                                      = 21
    ban                                               = 22
    unban                                             = 23
    member_update                                     = 24
    member_role_update                                = 25
    member_move                                       = 26
    member_disconnect                                 = 27
    bot_add                                           = 28
    role_create                                       = 30
    role_update                                       = 31
    role_delete                                       = 32
    invite_create                                     = 40
    invite_update                                     = 41
    invite_delete                                     = 42
    webhook_create                                    = 50
    webhook_update                                    = 51
    webhook_delete                                    = 52
    emoji_create                                      = 60
    emoji_update                                      = 61
    emoji_delete                                      = 62
    message_delete                                    = 72
    message_bulk_delete                               = 73
    message_pin                                       = 74
    message_unpin                                     = 75
    integration_create                                = 80
    integration_update                                = 81
    integration_delete                                = 82
    stage_instance_create                             = 83
    stage_instance_update                             = 84
    stage_instance_delete                             = 85
    sticker_create                                    = 90
    sticker_update                                    = 91
    sticker_delete                                    = 92
    scheduled_event_create                            = 100
    scheduled_event_update                            = 101
    scheduled_event_delete                            = 102
    thread_create                                     = 110
    thread_update                                     = 111
    thread_delete                                     = 112
    app_command_permission_update                     = 121
    soundboard_sound_create                           = 130
    soundboard_sound_update                           = 131
    soundboard_sound_delete                           = 132
    automod_rule_create                               = 140
    automod_rule_update                               = 141
    automod_rule_delete                               = 142
    automod_block_message                             = 143
    automod_flag_message                              = 144
    automod_timeout_member                            = 145
    creator_monetization_request_created              = 150
    creator_monetization_terms_accepted               = 151
    # fmt: on

    @property
    def category(self) -> Optional[AuditLogActionCategory]:
        # fmt: off
        lookup: Dict[AuditLogAction, Optional[AuditLogActionCategory]] = {
            AuditLogAction.guild_update:                             AuditLogActionCategory.update,
            AuditLogAction.channel_create:                           AuditLogActionCategory.create,
            AuditLogAction.channel_update:                           AuditLogActionCategory.update,
            AuditLogAction.channel_delete:                           AuditLogActionCategory.delete,
            AuditLogAction.overwrite_create:                         AuditLogActionCategory.create,
            AuditLogAction.overwrite_update:                         AuditLogActionCategory.update,
            AuditLogAction.overwrite_delete:                         AuditLogActionCategory.delete,
            AuditLogAction.kick:                                     None,
            AuditLogAction.member_prune:                             None,
            AuditLogAction.ban:                                      None,
            AuditLogAction.unban:                                    None,
            AuditLogAction.member_update:                            AuditLogActionCategory.update,
            AuditLogAction.member_role_update:                       AuditLogActionCategory.update,
            AuditLogAction.member_move:                              None,
            AuditLogAction.member_disconnect:                        None,
            AuditLogAction.bot_add:                                  None,
            AuditLogAction.role_create:                              AuditLogActionCategory.create,
            AuditLogAction.role_update:                              AuditLogActionCategory.update,
            AuditLogAction.role_delete:                              AuditLogActionCategory.delete,
            AuditLogAction.invite_create:                            AuditLogActionCategory.create,
            AuditLogAction.invite_update:                            AuditLogActionCategory.update,
            AuditLogAction.invite_delete:                            AuditLogActionCategory.delete,
            AuditLogAction.webhook_create:                           AuditLogActionCategory.create,
            AuditLogAction.webhook_update:                           AuditLogActionCategory.update,
            AuditLogAction.webhook_delete:                           AuditLogActionCategory.delete,
            AuditLogAction.emoji_create:                             AuditLogActionCategory.create,
            AuditLogAction.emoji_update:                             AuditLogActionCategory.update,
            AuditLogAction.emoji_delete:                             AuditLogActionCategory.delete,
            AuditLogAction.message_delete:                           AuditLogActionCategory.delete,
            AuditLogAction.message_bulk_delete:                      AuditLogActionCategory.delete,
            AuditLogAction.message_pin:                              None,
            AuditLogAction.message_unpin:                            None,
            AuditLogAction.integration_create:                       AuditLogActionCategory.create,
            AuditLogAction.integration_update:                       AuditLogActionCategory.update,
            AuditLogAction.integration_delete:                       AuditLogActionCategory.delete,
            AuditLogAction.stage_instance_create:                    AuditLogActionCategory.create,
            AuditLogAction.stage_instance_update:                    AuditLogActionCategory.update,
            AuditLogAction.stage_instance_delete:                    AuditLogActionCategory.delete,
            AuditLogAction.sticker_create:                           AuditLogActionCategory.create,
            AuditLogAction.sticker_update:                           AuditLogActionCategory.update,
            AuditLogAction.sticker_delete:                           AuditLogActionCategory.delete,
            AuditLogAction.scheduled_event_create:                   AuditLogActionCategory.create,
            AuditLogAction.scheduled_event_update:                   AuditLogActionCategory.update,
            AuditLogAction.scheduled_event_delete:                   AuditLogActionCategory.delete,
            AuditLogAction.thread_create:                            AuditLogActionCategory.create,
            AuditLogAction.thread_delete:                            AuditLogActionCategory.delete,
            AuditLogAction.thread_update:                            AuditLogActionCategory.update,
            AuditLogAction.app_command_permission_update:            AuditLogActionCategory.update,
            AuditLogAction.automod_rule_create:                      AuditLogActionCategory.create,
            AuditLogAction.automod_rule_update:                      AuditLogActionCategory.update,
            AuditLogAction.automod_rule_delete:                      AuditLogActionCategory.delete,
            AuditLogAction.automod_block_message:                    None,
            AuditLogAction.automod_flag_message:                     None,
            AuditLogAction.automod_timeout_member:                   None,
            AuditLogAction.creator_monetization_request_created:     None,
            AuditLogAction.creator_monetization_terms_accepted:      None,
            AuditLogAction.soundboard_sound_create:                  AuditLogActionCategory.create,
            AuditLogAction.soundboard_sound_update:                  AuditLogActionCategory.update,
            AuditLogAction.soundboard_sound_delete:                  AuditLogActionCategory.delete,
        }
        # fmt: on
        return lookup[self]

    @property
    def target_type(self) -> Optional[str]:
        v = self.value
        if v == -1:
            return 'all'
        elif v < 10:
            return 'guild'
        elif v < 20:
            return 'channel'
        elif v < 30:
            return 'user'
        elif v < 40:
            return 'role'
        elif v < 50:
            return 'invite'
        elif v < 60:
            return 'webhook'
        elif v < 70:
            return 'emoji'
        elif v == 73:
            return 'channel'
        elif v < 80:
            return 'message'
        elif v < 83:
            return 'integration'
        elif v < 90:
            return 'stage_instance'
        elif v < 93:
            return 'sticker'
        elif v < 103:
            return 'guild_scheduled_event'
        elif v < 113:
            return 'thread'
        elif v < 122:
            return 'integration_or_app_command'
        elif 139 < v < 143:
            return 'auto_moderation'
        elif v < 146:
            return 'user'
        elif v < 152:
            return 'creator_monetization'
