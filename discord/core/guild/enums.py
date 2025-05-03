

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


class TeamMembershipState(Enum):
    invited = 1
    accepted = 2


class TeamMemberRole(Enum):
    admin = 'admin'
    developer = 'developer'
    read_only = 'read_only'