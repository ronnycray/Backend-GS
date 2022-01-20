from services.finance.models import (
    FinancialTransaction,
    FinancialTag
)
from services.database import BaseModel
from sqlalchemy import select, update, join, exists, and_
from sqlalchemy.orm import scoped_session
from typing import List, Optional, Any


async def check_belongs_to_user_tag(
        db: scoped_session, tag_id: int, user_id: int
) -> bool:
    statement = select(FinancialTag).where(FinancialTag.id == tag_id)
    result = (await db.execute(statement)).scalars().all()
    if result:
        if result[0].financial_business.business.owner.user_id == user_id:
            return True

    return False


async def get_related_transactions(
        db: scoped_session, instance: Any
) -> Optional[List[FinancialTransaction]]:
    statement = (
        select(FinancialTransaction)
        .where(
            FinancialTransaction.id == instance.financial_business_id
        )
    )

    if instance.created_at_gte:
        statement = statement.where(
            FinancialTransaction.created_at >= instance.created_at_gte
        )

    if instance.created_at_lte:
        statement = statement.where(
            FinancialTransaction.created_at <= instance.created_at_lte
        )

    if instance.amount_gte:
        statement = statement.where(
            FinancialTransaction.amount >= instance.amount_gte
        )

    if instance.amount_lte:
        statement = statement.where(
            FinancialTransaction.amount <= instance.amount_gte
        )

    if instance.marker_color:
        statement = statement.where(
            FinancialTransaction.amount <= instance.amount_gte
        )

    result = (await db.execute(statement)).scalars().all()
    return result


async def get_tags_of_business(
        db: scoped_session, financial_business_id: int
) -> Optional[List[FinancialTag]]:
    statement = select(FinancialTag).where(FinancialTag.financial_business_id == financial_business_id)
    result = (await db.execute(statement)).scalars().all()
    return result
