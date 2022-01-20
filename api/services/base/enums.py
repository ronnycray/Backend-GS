import enum
import strawberry


@strawberry.enum
class StatusUserAccount(enum.Enum):
    """
    Status user account.

    ACTIVE: Active account that can manipulate with services
    NOT_ACTIVE: Account that need verified with confirmation code
    """
    ACTIVE = 'active'
    NOT_ACTIVE = 'not_active'
