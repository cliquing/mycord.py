from ....utils.enums import Enum

class InviteType(Enum):
    guild = 0
    group_dm = 1
    friend = 2


class InviteTarget(Enum):
    unknown = 0
    stream = 1
    embedded_application = 2