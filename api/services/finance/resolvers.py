from strawberry.types import Info
from services.work_with_db import (
    get_objects_by_field,
    delete_from_database,
    update_info,
    get_object_by_id
)
from services.finance.schema import (
    CreateMoneyMovementInputData, CreateMoneyMovementNode, CreateMoneyMovementErrorNode,
    CreateFinancialTagInputData, CreateFinancialTagNode, CreateFinancialTagErrorNode,
    UpdateFinancialTagInputData, UpdateFinancialTagNode, UpdateFinancialTagErrorNode,
    DeleteFinancialTagInputData, DeleteFinancialTagNode, DeleteFinancialTagErrorNode,
    GetHistoryTransactionsInputData, HistoryTransactionsNode,
    GetFinancialTagsInputData, FinancialTagsNode
)
from services.business.work_with_db import (
    check_user_that_he_is_owner,
)
from services.finance.work_with_db import (
    check_belongs_to_user_tag,
    get_related_transactions,
    get_tags_of_business
)
from services.finance.models import (
    FinancialTransaction, TransactionTag, FinancialTag
)
import secrets


async def get_hash_id_for_transaction(db) -> str:
    hash_id = secrets.token_hex(nbytes=20)
    while (
            await get_objects_by_field(
                db=db, model=FinancialTransaction,
                field=FinancialTransaction.hash_id,
                value=hash_id
            )
    ):
        hash_id = secrets.token_hex(nbytes=20)

    return hash_id


async def create_money_movement_resolver(
        info: Info, input_data: CreateMoneyMovementInputData
) -> CreateMoneyMovementNode:
    instance = input_data.to_pydantic()
    context = info.context
    created = False
    transaction = None
    error = None

    necessary_points_exists = (
        True if instance.expense_category_id or instance.accrual_category_id else False
    )
    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            financial_business_id=instance.financial_business_id
        )
    )

    if necessary_points_exists and user_is_owner_business:
        hash_id = await get_hash_id_for_transaction(db=context.db)
        new_transaction = FinancialTransaction(
            financial_business_id=instance.financial_business_id,
            hash_id=hash_id
        )
        context.db.add(new_transaction)
        await context.db.commit()

        if instance.tags:
            for tag_id in instance.tags:
                new_transaction_tag = TransactionTag(
                    transaction_hash_id=hash_id,
                    tag_id=tag_id
                )
                context.db.add(new_transaction_tag)

        await update_info(
            db=context.db, model=FinancialTransaction,
            object_id=new_transaction.id,
            input_data=instance.dict(
                exclude_unset=True, exclude_none=True,
                exclude={'financial_business_id', 'tags'}
            )
        )
        await context.db.commit()

        transaction = (
            await get_object_by_id(
                db=context.db,
                model=FinancialTransaction,
                object_id=new_transaction.id
            )
        )

    elif not necessary_points_exists:
        error = CreateMoneyMovementErrorNode(
            code=CreateMoneyMovementErrorNode.CreateMoneyMovementErrorCode.EXPENSE_OR_ACCRUAL_IS_EMPTY,
            messsage='Expense or accrual must have in request'
        )

    elif not user_is_owner_business:
        error = CreateMoneyMovementErrorNode(
            code=CreateMoneyMovementErrorNode.CreateMoneyMovementErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            messsage="User is not owner business"
        )

    return CreateMoneyMovementNode(created=created, transaction=transaction, error=error)


async def create_financial_tag_resolver(
        info: Info, input_data: CreateFinancialTagInputData
) -> CreateFinancialTagNode:
    instance = input_data.to_pydantic()
    context = info.context
    created = False
    tag = None
    error = None

    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            financial_business_id=instance.financial_business_id
        )
    )

    tag_name_exists = (
        await get_objects_by_field(
            db=context.db,
            model=FinancialTag,
            field=FinancialTag.name,
            value=instance.name
        )
    )

    if user_is_owner_business and not tag_name_exists:
        new_tag = FinancialTag(
            financial_business_id=instance.financial_business_id,
            name=instance.name
        )
        context.db.add(new_tag)
        await context.db.commit()

        tag = (
            await get_object_by_id(
                db=context.db,
                model=FinancialTag,
                object_id=new_tag.id
            )
        )

    elif not user_is_owner_business:
        error = CreateFinancialTagErrorNode(
            code=CreateFinancialTagErrorNode.CreateFinancialTagErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            messsage="User is not owner business"
        )

    elif tag_name_exists:
        error = CreateFinancialTagErrorNode(
            code=CreateFinancialTagErrorNode.CreateFinancialTagErrorCode.TAG_NAME_EXISTS,
            messsage="Tag name exists"
        )

    return CreateFinancialTagNode(created=created, tag=tag, error=error)


async def update_financial_tag_resolver(
        info: Info, input_data: UpdateFinancialTagInputData
) -> UpdateFinancialTagNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    tag = None
    error = None

    tag_exists_and_belongs_to_user = (
        await check_belongs_to_user_tag(
            db=context.db,
            tag_id=instance.tag_id,
            user_id=context.user.id
        )
    )

    if tag_exists_and_belongs_to_user:
        tag = (
            await update_info(
                db=context.db,
                model=FinancialTag,
                object_id=instance.tag_id,
                input_data=instance.dict(
                    exclude_unset=True, exclude_none=True,
                    exclude={"tag_id"}
                )
            )
        )
        updated = True

    else:
        error = UpdateFinancialTagErrorNode(
            code=UpdateFinancialTagErrorNode.UpdateFinancialTagErrorCode.USER_IS_NOT_OWNER_TAG,
            message='Tag not belongs to user'
        )

    return UpdateFinancialTagNode(update=updated, tag=tag, error=error)


async def delete_financial_tag_resolver(
        info: Info, input_data: DeleteFinancialTagInputData
) -> DeleteFinancialTagNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    tag_exists_and_belongs_to_user = (
        await check_belongs_to_user_tag(
            db=context.db,
            tag_id=instance.tag_id,
            user_id=context.user.id
        )
    )

    if tag_exists_and_belongs_to_user:
        deleted = (
            await delete_from_database(
                db=context.db, model=FinancialTag,
                object_id=instance.tag_id
            )
        )

    else:
        error = DeleteFinancialTagErrorNode(
            code=DeleteFinancialTagErrorNode.DeleteFinancialTagErrorCode.USER_IS_NOT_OWNER_TAG,
            message='Tag not belongs to user'
        )

    return DeleteFinancialTagNode(deleted=deleted, error=error)


async def get_history_transactions_resolver(
        info: Info, input_data: GetHistoryTransactionsInputData
) -> HistoryTransactionsNode:
    instance = input_data.to_pydantic()
    context = info.context
    count = 0
    related_transactions = list()

    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            financial_business_id=instance.financial_business_id
        )
    )

    if user_is_owner_business:
        related_transactions = (
            await get_related_transactions(
                db=context.db,
                instance=instance
            )
        )
        count = len(related_transactions)

    return HistoryTransactionsNode(count=count, transactions=related_transactions)


async def get_financial_tags_resolver(
        info: Info, input_data: GetFinancialTagsInputData
) -> FinancialTagsNode:
    instance = input_data.to_pydantic()
    context = info.context
    related_tags = list()

    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            financial_business_id=instance.financial_business_id
        )
    )

    if user_is_owner_business:
        related_tags = (
            await get_tags_of_business(
                db=context.db,
                financial_business_id=instance.financial_business_id
            )
        )

    return FinancialTagsNode(tags=related_tags)
