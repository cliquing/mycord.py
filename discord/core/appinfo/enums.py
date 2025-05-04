from ...utils.enums import Enum

class AppCommandOptionType(Enum):
    subcommand = 1
    subcommand_group = 2
    string = 3
    integer = 4
    boolean = 5
    user = 6
    channel = 7
    role = 8
    mentionable = 9
    number = 10
    attachment = 11


class AppCommandType(Enum):
    chat_input = 1
    user = 2
    message = 3


class AppCommandPermissionType(Enum):
    role = 1
    user = 2
    channel = 3


class TeamMembershipState(Enum):
    invited = 1
    accepted = 2


class TeamMemberRole(Enum):
    admin = 'admin'
    developer = 'developer'
    read_only = 'read_only'