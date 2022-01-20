from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import (
    Column, Integer, ForeignKey, VARCHAR, Enum, TIMESTAMP
)
from sqlalchemy.orm import relationship
from services.database import BaseModel
from .enums import StatusUserAccount
from datetime import datetime, timedelta
from services.config import get_settings

from services.business.models import Business, Client, TeamMember
from services.event_calendar.models import CalendarEvent


def define_expire() -> datetime:
    jwt_setting = get_settings()
    expire_at = datetime.now() + timedelta(minutes=jwt_setting.refresh_token_expire_minutes)
    return expire_at


class User(BaseModel):
    __tablename__ = 'user'
    __tableargs__ = {
        'comment': "Main table for user instance in system"
    }

    first_name = Column(VARCHAR(255), nullable=False, default="")
    second_name = Column(VARCHAR(255), nullable=False, default="")
    middle_name = Column(VARCHAR(255), nullable=False, default="")
    email = Column(VARCHAR(255), nullable=False, unique=True, default="")
    phone = Column(VARCHAR(255), nullable=False, default="")
    password = Column(VARCHAR(255), nullable=False, default="")
    birthday = Column(TIMESTAMP, nullable=False, default=datetime.now())
    profile_picture = Column(VARCHAR(255), nullable=False, default="")
    account_status = Column(
        Enum(StatusUserAccount, native_enum=False),
        nullable=False,
        default=StatusUserAccount.NOT_ACTIVE
    )

    businesses = relationship(lambda: Business, lazy='selectin', back_populates="owner", uselist=True)
    events = relationship(lambda: CalendarEvent, lazy='selectin', back_populates="owner", uselist=True)
    clients = relationship(lambda: Client, lazy='selectin', foreign_keys='[Client.user_id]')
    credentials = relationship('ThirdPartyAuthentication', lazy='selectin', uselist=False)
    devices = relationship('Devices', lazy='selectin', uselist=True)
    teams_member = relationship(lambda: TeamMember, lazy='selectin', foreign_keys='[TeamMember.user_id]', uselist=True)

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'UserID: {self.id} | Email:{self.email}'

    @staticmethod
    def set_password(password: str) -> str:
        password = generate_password_hash(password=password)

        return password

    @staticmethod
    def check_password(password: str, hash_password: str) -> bool:
        return check_password_hash(pwhash=hash_password, password=password)


class ThirdPartyAuthentication(BaseModel):
    __tablename__ = 'third_party_authentication'
    __tableargs__ = {
        'comment': "Table with conditionals of user in any system"
    }

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True
    )
    google_uid = Column(VARCHAR(255), nullable=False, default="")

    user = relationship('User', back_populates='credentials')

    def __repr__(self):
        return f'UserID: {self.user_id} | Google ID: {self.google_uid}'


class RefreshToken(BaseModel):
    __tablename__ = 'refresh_tokens'
    __tableargs__ = {
        'comment': "Table for refresh access tokens user"
    }

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    refresh_token = Column(VARCHAR(255), nullable=False, unique=True)
    expires_at = Column(TIMESTAMP,
                        nullable=False,
                        default=define_expire)

    user = relationship('User', cascade="all,delete")


class Devices(BaseModel):
    __tablename__ = 'devices'
    __tableargs__ = {
        'comment': "Table of devices ID user"
    }

    user_id = Column(Integer, ForeignKey('user.id'))
    device_id = Column(VARCHAR(255), nullable=False)
    last_authentication = Column(TIMESTAMP,
                                 nullable=False,
                                 default=datetime.now)

    user = relationship('User', cascade="all,delete", back_populates='devices')
