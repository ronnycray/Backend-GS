import enum
from typing import Optional, List

from services.config import get_settings

import strawberry
from services.schema import ErrorNode
from pydantic import BaseModel, constr, EmailStr
from datetime import datetime
from services.base.enums import StatusUserAccount
from services.business.schema import BusinessNode
from services.event_calendar.schema import EventNode


settings = get_settings()


@strawberry.type
class DeviceNode:
    device_id: str
    last_authentication: datetime


@strawberry.type
class UserNode:
    id: int
    email: str
    created_at: datetime
    updated_at: datetime
    account_status: StatusUserAccount
    devices: List[DeviceNode]
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    middle_name: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[datetime] = None
    profile_picture: Optional[str] = None
    businesses: Optional[List[BusinessNode]] = None
    events: Optional[List[EventNode]] = None


@strawberry.type
class RegistrationError(ErrorNode):
    @strawberry.enum
    class RegistrationErrorCode(enum.Enum):
        EMAIL_TAKEN = "email_taken"
        NOT_CREATED = "not_created"

    code: RegistrationErrorCode


@strawberry.type
class AuthenticationError(ErrorNode):
    @strawberry.enum
    class AuthenticationErrorCode(enum.Enum):
        WRONG_CREDENTIALS = "wrong_credentials"

    code: AuthenticationErrorCode


@strawberry.type
class ThirdPartyAuthenticationError(ErrorNode):
    @strawberry.enum
    class ThirdPartyAuthenticationErrorCode(enum.Enum):
        UID_EXISTS = 'uid_exists'
        WRONG_CREDENTIALS = "wrong_credentials"

    code: ThirdPartyAuthenticationErrorCode


@strawberry.type
class RefreshTokenError(ErrorNode):
    @strawberry.enum
    class RefreshTokenErrorCode(enum.Enum):
        EXPIRED = "expired"
        INVALID = "invalid"

    code: RefreshTokenErrorCode


@strawberry.type
class UpdateUserError(ErrorNode):
    @strawberry.enum
    class UpdateUserErrorCode(enum.Enum):
        EMPTY_FIELDS = 'empty_fields'

    code: UpdateUserErrorCode


@strawberry.type
class RegistrationNode:
    registration_success: bool
    user: Optional[UserNode]
    token: Optional[str]
    token_refresh: Optional[str]
    error: Optional[RegistrationError]


@strawberry.type
class AuthenticationNode:
    authentication_status: bool
    token: Optional[str]
    token_refresh: Optional[str]
    error: Optional[AuthenticationError]


@strawberry.type
class ThirdPartyAuthenticationNode:
    status: bool
    token: Optional[str]
    token_refresh: Optional[str]
    error: Optional[ThirdPartyAuthenticationError]


@strawberry.type
class RefreshTokenNode:
    access_token: Optional[str]
    refresh_token: Optional[str]
    error: Optional[RefreshTokenError]


@strawberry.type
class UpdateUserNode:
    updated: bool
    user: Optional[UserNode]
    error: Optional[UpdateUserError]


@strawberry.type
class GetMeNode:
    user: UserNode
    error: Optional[ErrorNode]


class RegistrationData(BaseModel):
    email: EmailStr
    password: constr(max_length=20, min_length=8)
    device_id: constr(max_length=settings.length_device_id)
    uid: Optional[constr(max_length=settings.length_google_uid)]
    display_name: Optional[constr(max_length=30)]
    profile_picture: Optional[str]
    account_status: Optional[StatusUserAccount]


class AuthenticationData(BaseModel):
    email: EmailStr
    password: constr(max_length=20, min_length=8)


class ThirdPartyAuthenticationData(BaseModel):
    email: EmailStr
    uid: constr(max_length=settings.length_google_uid)
    device_id: constr(max_length=settings.length_device_id)
    display_name: Optional[constr(max_length=30)]
    profile_picture: Optional[str]
    account_status: Optional[StatusUserAccount]


class RefreshTokenData(BaseModel):
    token: str


class UpdateUserData(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    middle_name: Optional[str]
    phone: Optional[str]
    birthday: Optional[datetime]
    email: Optional[EmailStr]


@strawberry.experimental.pydantic.input(model=RegistrationData, fields=[
    "email",
    "password",
    "device_id",
    "uid",
    "display_name",
    "profile_picture",
    "account_status"
])
class RegistrationInputData:
    pass


@strawberry.experimental.pydantic.input(model=AuthenticationData, fields=[
    "email",
    "password"
])
class AuthenticationInputData:
    pass


@strawberry.experimental.pydantic.input(model=ThirdPartyAuthenticationData, fields=[
    "email",
    "uid",
    "device_id",
    "display_name",
    "profile_picture",
    "account_status"
])
class ThirdPartyAuthenticationInputData:
    pass


@strawberry.experimental.pydantic.input(model=RefreshTokenData, fields=[
    "token"
])
class RefreshTokenInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateUserData, fields=[
    "first_name",
    "second_name",
    "middle_name",
    "phone",
    "birthday",
    "email"
])
class UpdateUserInputData:
    pass
