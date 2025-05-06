from ...utils.enums import Enum

class SpeakingState(Enum):
    none = 0
    voice = 1
    soundshare = 2
    priority = 4

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value
    

class StatusType(Enum):
    online = 'online'
    offline = 'offline'
    idle = 'idle'
    dnd = 'dnd'
    do_not_disturb = 'dnd'
    invisible = 'invisible'

    def __str__(self) -> str:
        return self.value