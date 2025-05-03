

class SKUType(Enum):
    durable = 2
    consumable = 3
    subscription = 5
    subscription_group = 6


class EntitlementType(Enum):
    purchase = 1
    premium_subscription = 2
    developer_gift = 3
    test_mode_purchase = 4
    free_purchase = 5
    user_gift = 6
    premium_purchase = 7
    application_subscription = 8


class EntitlementOwnerType(Enum):
    guild = 1
    user = 2