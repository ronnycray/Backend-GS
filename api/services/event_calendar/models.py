from sqlalchemy import (
    Column, Integer, ForeignKey, VARCHAR, TIMESTAMP, TIME
)
from sqlalchemy.orm import relationship
from services.database import BaseModel
from datetime import datetime


def now_time():
    return datetime.now().time()


class CalendarEvent(BaseModel):
    __tablename__ = 'calendar_event'
    __tableargs__ = {
        'comment': "Table of user event calendars"
    }

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )
    event_name = Column(VARCHAR(255), nullable=False, default="")
    event_description = Column(VARCHAR(1024), nullable=False, default="")
    event_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    event_from_time = Column(TIME, nullable=False, default=now_time)
    event_to_time = Column(TIME, nullable=False, default=now_time)
    business_id = Column(
        Integer,
        ForeignKey('business.id', ondelete='CASCADE')
    )

    owner = relationship("User", lazy='selectin', foreign_keys=[user_id], back_populates="events")
    business = relationship("Business", lazy='selectin', foreign_keys=[business_id], back_populates="events")
    participants = relationship("Participant", lazy='selectin', foreign_keys='[Participant.event_id]', uselist=True)

    def __repr__(self):
        return f"Event of user ID: {self.user_id}"


class Participant(BaseModel):
    __tablename__ = 'participant'
    __tableargs__ = {
        'comment': "Table of event calendars participants"
    }

    event_id = Column(
        Integer,
        ForeignKey('calendar_event.id', ondelete='CASCADE')
    )
    client_id = Column(
        Integer,
        ForeignKey('client.id', ondelete='CASCADE')
    )
    client_email = Column(
        VARCHAR(255), nullable=False, default=""
    )

    client = relationship("Client", lazy='selectin', foreign_keys=[client_id], back_populates="events", uselist=False)
    event = relationship("CalendarEvent", lazy='selectin', foreign_keys=[event_id], back_populates="participants")

    def __repr__(self):
        return f"Participant of client ID: {self.client_id} | {self.client_email}"
