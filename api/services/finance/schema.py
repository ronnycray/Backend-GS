import enum
from typing import Optional, List

import strawberry
from services.schema import ErrorNode
from pydantic import BaseModel, constr
from datetime import datetime
from services.finance.enums import TransactionType, ColorActions


@strawberry.type
class TagNode:
    id: int
    name: str


@strawberry.type
class TransactionTag:
    id: int
    tag: TagNode


@strawberry.type
class ExpenseNode:
    title: str
    color: ColorActions
    image: str


@strawberry.type
class AccrualNode:
    title: str
    color: ColorActions
    image: str


@strawberry.type
class TransactionNode:
    hash_id: str
    transaction_type: TransactionType
    amount: float
    date: datetime
    expense: Optional[ExpenseNode]
    accrual: Optional[AccrualNode]
    transactions_tags: Optional[List[TransactionTag]]
    comment: Optional[str]


@strawberry.type
class FinanceAccount:
    total_amount: float
    accrual_categories: Optional[List[AccrualNode]]
    expense_categories: Optional[List[ExpenseNode]]
    tags: Optional[List[TagNode]]
    transactions: Optional[List[TransactionNode]]


@strawberry.type
class CreateMoneyMovementErrorNode(ErrorNode):
    @strawberry.enum
    class CreateMoneyMovementErrorCode(enum.Enum):
        NOT_CREATED = 'not_created'
        EXPENSE_OR_ACCRUAL_IS_EMPTY = 'expense_or_accrual_is_empty'
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'

    code: CreateMoneyMovementErrorCode


@strawberry.type
class CreateFinancialTagErrorNode(ErrorNode):
    @strawberry.enum
    class CreateFinancialTagErrorCode(enum.Enum):
        NOT_CREATED = 'not_created'
        TAG_NAME_EXISTS = 'tag_name_exists'
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'

    code: CreateFinancialTagErrorCode


@strawberry.type
class UpdateFinancialTagErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateFinancialTagErrorCode(enum.Enum):
        NOT_UPDATED = 'not_updated'
        USER_IS_NOT_OWNER_TAG = 'user_is_not_owner_tag'

    code: UpdateFinancialTagErrorCode


@strawberry.type
class DeleteFinancialTagErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteFinancialTagErrorCode(enum.Enum):
        NOT_UPDATED = 'not_updated'
        USER_IS_NOT_OWNER_TAG = 'user_is_not_owner_tag'

    code: DeleteFinancialTagErrorCode


@strawberry.type
class CreateMoneyMovementNode:
    created: bool
    transaction: Optional[TransactionNode]
    error: Optional[CreateMoneyMovementErrorNode]


@strawberry.type
class CreateFinancialTagNode:
    created: bool
    tag: Optional[TagNode]
    error: Optional[CreateFinancialTagErrorNode]


@strawberry.type
class UpdateFinancialTagNode:
    updated: bool
    tag: Optional[TagNode]
    error: Optional[UpdateFinancialTagErrorNode]


@strawberry.type
class DeleteFinancialTagNode:
    deleted: bool
    error: Optional[DeleteFinancialTagErrorNode]


@strawberry.type
class HistoryTransactionsNode:
    count: int
    transactions: List[Optional[TransactionNode]]


@strawberry.type
class FinancialTagsNode:
    tags: List[Optional[TagNode]]


class CreateMoneyMovementData(BaseModel):
    financial_business_id: int
    transaction_type: TransactionType
    amount: float
    date: datetime
    expense_category_id: Optional[int]
    accrual_category_id: Optional[int]
    comment: Optional[constr(max_length=500)]
    tags: Optional[List[int]]


class CreateFinancialTagData(BaseModel):
    financial_business_id: int
    name: constr(max_length=100)


class UpdateFinancialTagData(BaseModel):
    tag_id: int
    name: constr(max_length=100)


class DeleteFinancialTagData(BaseModel):
    tag_id: int


class GetHistoryTransactionsData(BaseModel):
    financial_business_id: Optional[int]
    created_at_gte: Optional[datetime]
    created_at_lte: Optional[datetime]
    amount_gte: Optional[int]
    amount_lte: Optional[int]
    marker_color: Optional[ColorActions]


class GetFinancialTagsData(BaseModel):
    financial_business_id: Optional[int]


@strawberry.experimental.pydantic.input(model=CreateMoneyMovementData, fields=[
    "financial_business_id",
    "transaction_type",
    "amount",
    "date",
    "expense_category_id",
    "accrual_category_id",
    "comment",
    "tags"
])
class CreateMoneyMovementInputData:
    pass


@strawberry.experimental.pydantic.input(model=CreateFinancialTagData, fields=[
    "financial_business_id",
    "name"
])
class CreateFinancialTagInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateFinancialTagData, fields=[
    "tag_id",
    "name"
])
class UpdateFinancialTagInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteFinancialTagData, fields=[
    "tag_id"
])
class DeleteFinancialTagInputData:
    pass


@strawberry.experimental.pydantic.input(model=GetHistoryTransactionsData, fields=[
    "financial_business_id",
    "created_at_gte",
    "created_at_lte",
    "amount_at_gte",
    "amount_at_lte"
])
class GetHistoryTransactionsInputData:
    pass


@strawberry.experimental.pydantic.input(model=GetFinancialTagsData, fields=[
    "financial_business_id"
])
class GetFinancialTagsInputData:
    pass
