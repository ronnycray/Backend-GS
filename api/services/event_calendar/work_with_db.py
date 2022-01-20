from services.event_calendar.models import (
    CalendarEvent,
    Participant
)
from services.database import BaseModel
from sqlalchemy import select, update, join, exists, and_
from sqlalchemy.orm import scoped_session
from typing import List, Optional
from datetime import datetime


async def check_event_exists(
        db: scoped_session, user_id: int, event_id: int
) -> bool:
    statement = (
        exists(CalendarEvent)
        .where(
            and_(
                CalendarEvent.id == event_id,
                CalendarEvent.user_id == user_id
            )
        )
    ).select()
    result = (await db.execute(statement)).scalars().one()
    return result


async def check_belong_participant_to_user(
        db: scoped_session, participant_id: int, user_id: int
) -> bool:
    join_business = join(Participant, CalendarEvent, Participant.event_id == CalendarEvent.id)
    statement = (
        select(Participant)
        .where(Participant.id == participant_id)
        .select_from(join_business)
    )
    result = (await db.execute(statement)).scalars().all()
    if result:
        event = result[0]
        if event.user_id == user_id:
            return True
    return False


async def get_related_events(
        db: scoped_session, user_id: int,
        from_date: Optional[datetime] = None, to_date: Optional[datetime] = None
) -> Optional[list]:
    if from_date and to_date:
        statement = (
            select(CalendarEvent)
            .where(
                and_(
                    CalendarEvent.event_date >= from_date,
                    CalendarEvent.event_date <= to_date,
                    CalendarEvent.user_id == user_id
                )
            )
        )

    elif from_date:
        statement = (
            select(CalendarEvent)
            .where(
                CalendarEvent.event_date >= from_date,
                CalendarEvent.user_id == user_id
            )
        )

    elif to_date:
        statement = (
            select(CalendarEvent)
            .where(
                CalendarEvent.event_date <= to_date,
                CalendarEvent.user_id == user_id
            )
        )

    else:
        statement = (
            select(CalendarEvent)
            .where(
                CalendarEvent.user_id == user_id
            )
        )

    result = (await db.execute(statement)).scalars().all()
    return result
