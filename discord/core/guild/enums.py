from ...utils.enums import Enum

class PrivacyLevel(Enum):
    guild_only = 2


class NSFWLevel(Enum, comparable=True):
    default = 0
    explicit = 1
    safe = 2
    age_restricted = 3


class MFALevel(Enum, comparable=True):
    disabled = 0
    require_2fa = 1


class EventStatus(Enum):
    scheduled = 1
    active = 2
    completed = 3
    canceled = 4

    ended = 3
    cancelled = 4


class NotificationLevel(Enum, comparable=True):
    all_messages = 0
    only_mentions = 1


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
    



class TeamMembershipState(Enum):
    invited = 1
    accepted = 2


class TeamMemberRole(Enum):
    admin = 'admin'
    developer = 'developer'
    read_only = 'read_only'



class ExpireBehaviour(Enum):
    remove_role = 0
    kick = 1


ExpireBehavior = ExpireBehaviour


class EntityType(Enum):
    stage_instance = 1
    voice = 2
    external = 3