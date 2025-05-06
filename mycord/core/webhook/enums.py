from ...utils.enums import Enum

class WebhookType(Enum):
    incoming = 1
    channel_follower = 2
    application = 3