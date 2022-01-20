import enum
import strawberry


@strawberry.enum
class ColorActions(enum.Enum):
    """
    All colors of action financial businesses
    ex: RED, YELLOW, BLUE etc..
    """
    RED = 'red'
    YELLOW = 'yellow'
    PURPLE = 'purple'
    BLUE = 'blue'
    PINK = 'pink'
    GREEN = 'green'


@strawberry.enum
class TransactionType(enum.Enum):
    """
    Transaction types
    """
    EXPENSE = 'expense'
    ACCRUAL = 'accrual'
