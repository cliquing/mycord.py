from ...utils.enums import Enum

class InteractionType(Enum):
    ping = 1
    application_command = 2
    component = 3
    autocomplete = 4
    modal_submit = 5


class InteractionResponseType(Enum):
    pong = 1
    # ack = 2 (deprecated)
    # channel_message = 3 (deprecated)
    channel_message = 4  # (with source)
    deferred_channel_message = 5  # (with source)
    deferred_message_update = 6  # for components
    message_update = 7  # for components
    autocomplete_result = 8
    modal = 9  # for modals
    # premium_required = 10 (deprecated)