import enum
import strawberry


@strawberry.enum
class BusinessStatus(enum.Enum):
    """
    Status of business.

    All existing status of businesses in the system are listed here
    """
    ACTIVE = 'active'
    NOT_ACTIVE = 'not_active'


@strawberry.enum
class RolePrivileges(enum.Enum):
    """
    Privileges of business roles

    All available privileges for the business role are listed here
    """
    ALL_ACCESS = 'all_access'
    READ_ONLY = 'read_only'


@strawberry.enum
class MemberType(enum.Enum):
    """
    Type of team member

    There are 2 main types - the owner and the staff
    """
    OWNER = 'owner'
    STAFF = 'staff'


@strawberry.enum
class UserTypeForBusiness(enum.Enum):
    """
    User type for business

    The type takes the values: INDIVIDUAL, LLC, SOLE_PROPRIETOR
    """
    INDIVIDUAL = 'individual'
    LLC = 'llc'
    SOLE_PROPRIETOR = 'sole_proprietor'


@strawberry.enum
class StatusUserForBusiness(enum.Enum):
    """
    Status of user for business owner
    """
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    IN_ARCHIVE = 'in_archive'
