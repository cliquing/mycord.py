from ....utils.enums import Enum

class AutoModRuleTriggerType(Enum):
    keyword = 1
    harmful_link = 2
    spam = 3
    keyword_preset = 4
    mention_spam = 5
    member_profile = 6


class AutoModRuleEventType(Enum):
    message_send = 1
    member_update = 2


class AutoModRuleActionType(Enum):
    block_message = 1
    send_alert_message = 2
    timeout = 3
    block_member_interactions = 4