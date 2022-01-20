from services.business.models import (
    Business,
    ScopeTypeBusiness,
    BusinessRoles,
    TeamMember,
    Client
)
from services.finance.models import (
    FinancialBusiness
)
from services.database import BaseModel
from sqlalchemy import select, update, join, exists, and_
from sqlalchemy.orm import scoped_session
from typing import List, Optional


async def update_info_business(
        db: scoped_session, business_id: int, input_data: dict
) -> Business:
    update_statement = (
        update(Business)
        .where(Business.id == business_id)
        .values(**input_data).returning(Business)
    )
    result = await db.execute(update_statement)

    return result.fetchall()[0]


async def get_scoped_business_types_from_db(db: scoped_session) -> List[ScopeTypeBusiness]:
    statement = select(ScopeTypeBusiness)
    result = (await db.execute(statement)).scalars().all()
    return result


async def check_user_that_he_is_owner(
        db: scoped_session, user_id: int,
        business_id: Optional[int] = None, team_member_id: Optional[int] = None,
        financial_business_id: Optional[int] = None
) -> bool:
    result = False
    if business_id:
        statement = (
            exists(Business)
            .where(
                and_(
                    Business.id == business_id,
                    Business.user_id == user_id)
            )
        ).select()
        result = (await db.execute(statement)).scalars().one()

    elif team_member_id:
        statement = select(TeamMember).where(TeamMember.id == team_member_id)
        result_statement = (await db.execute(statement)).scalars().all()
        if result_statement:
            team_member = result_statement[0]
            if team_member.business.user_id == user_id:
                result = True

    elif financial_business_id:
        statement = (
            select(FinancialBusiness)
            .where(FinancialBusiness.id == financial_business_id)
        )
        result_statement = (await db.execute(statement)).scalars().all()
        if result_statement:
            financial_business = result_statement[0]
            if financial_business.business.user_id == user_id:
                result = True

    return result


async def check_user_that_he_is_owner_role(
        db: scoped_session, user_id: int,
        role_id: Optional[int] = None, team_member_id: Optional[int] = None
) -> bool:
    is_owner = False
    if role_id:
        join_business = join(BusinessRoles, Business, BusinessRoles.business_id == Business.id)
        statement = (
            select(BusinessRoles)
            .where(BusinessRoles.id == role_id)
            .select_from(join_business)
        )
        result = (await db.execute(statement)).scalars().all()
        if result:
            role = result[0]
            if role.business.user_id == user_id:
                is_owner = True

    elif team_member_id:
        statement = select(TeamMember).where(TeamMember.id == team_member_id)
        result_statement = (await db.execute(statement)).scalars().all()
        if result_statement:
            team_member = result_statement[0]
            if team_member.role.business.user_id == user_id:
                is_owner = True

    return is_owner


async def check_team_member_exists(db: scoped_session, team_member_id: int, business_id: int) -> bool:
    statement = exists(TeamMember).where(
        and_(
            TeamMember.business_id == business_id,
            TeamMember.user_id == team_member_id
        )
    ).select()
    result = (await db.execute(statement)).scalars().one()
    return result


async def get_client_of_user(db: scoped_session, client_id: int, user_id: int) -> bool:
    statement = (
        exists(Client)
        .where(
            and_(
                Client.id == client_id,
                Client.user_id == user_id
            )
        )
    ).select()
    result = (await db.execute(statement)).scalars().one()
    return result


async def get_clients_from_db(db: scoped_session, user_id: int) -> Optional[List[Client]]:
    statement = select(Client).where(Client.user_id == user_id)
    result = (await db.execute(statement)).scalars().all()
    return result


async def get_business_team(db: scoped_session, business_id: int) -> Optional[List[TeamMember]]:
    statement = select(TeamMember).where(TeamMember.business_id == business_id)
    result = (await db.execute(statement)).scalars().all()
    return result


async def client_belongs_to_user_check(
        db: scoped_session, user_id: int, client_id: int
) -> bool:
    statement = exists(Client).where(
        and_(
            Client.id == client_id,
            Client.user_id == user_id
        )
    ).select()
    result = (await db.execute(statement)).scalars().one()
    return result
