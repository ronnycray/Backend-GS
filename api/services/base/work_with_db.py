from services.base.models import User, RefreshToken, Devices, TeamMember
from services.event_calendar.models import Participant
from sqlalchemy import insert, select, update, exists
from sqlalchemy.orm import scoped_session
from services.config import get_settings
from datetime import datetime, timedelta


async def get_user(db: scoped_session, field, value):
    statement = select(User).where(field == value)
    user = await db.execute(statement)

    return user.scalars().all()


async def refresh_token_exists(db: scoped_session, token: str) -> bool:
    statement = exists(RefreshToken).where(RefreshToken.refresh_token == token).select()
    exists_result = (await db.execute(statement)).scalars().one()
    return exists_result


async def create_refresh_token(db: scoped_session, user_id: int, refresh_token: str) -> RefreshToken:
    statement = insert(RefreshToken).values(user_id=user_id,
                                            refresh_token=refresh_token).returning(RefreshToken)
    result = await db.execute(statement)
    refresh_token_object = result.fetchall()[0]
    return refresh_token_object


async def update_refresh_token(db: scoped_session, id_token: int, new_refresh_token: str) -> RefreshToken:
    jwt_setting = get_settings()
    expires_at = datetime.now() + timedelta(
                    minutes=jwt_setting.refresh_token_expire_minutes
                )
    statement = update(RefreshToken).where(RefreshToken.id == id_token).values(
        refresh_token=new_refresh_token,
        expires_at=expires_at
    ).returning(RefreshToken)
    result = await db.execute(statement)
    refresh_token_object = result.fetchall()[0]

    return refresh_token_object


async def update_device_of_user(db: scoped_session, user: User, device_id: str):
    statement = select(Devices).where(Devices.device_id == device_id)
    result = (await db.execute(statement)).scalars().all()
    if not result:
        device = Devices(
            user_id=user.id,
            device_id=device_id
        )
        db.add(device)
    else:
        update_statement = (
            update(Devices)
            .where(Devices.device_id == device_id)
            .values(
                user_id=user.id,
                last_authentication=datetime.now()
            )
        )
        await db.execute(update_statement)


async def update_user_info(db: scoped_session, user: User, instance: dict) -> User:
    statement = (
        update(User)
        .where(User.id == user.id)
        .values(**instance)
        .returning(User)
    )
    result = await db.execute(statement)

    return result.fetchall()[0]


async def add_user(db: scoped_session, instance: dict) -> User:
    statement = (
        insert(User)
        .values(**instance)
        .returning(User)
    )
    result = await db.execute(statement)

    return result.fetchall()[0]


async def fill_in_related_services_by_user(db: scoped_session, user: User):
    statement_team_member = (
        update(TeamMember)
        .where(TeamMember.email == user.email)
        .values(user_id=user.id)
    )
    await db.execute(statement_team_member)
