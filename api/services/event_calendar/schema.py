import enum
from typing import Optional, List

import strawberry
from services.schema import ErrorNode
from services.business.schema import ClientNode, BusinessNode
from pydantic import BaseModel, constr
from datetime import datetime, time


@strawberry.type
class ParticipantNode:
    id: int
    client: Optional[ClientNode]


@strawberry.type
class EventNode:
    id: int
    event_name: str
    event_description: str
    event_date: datetime
    event_from_time: Optional[time]
    event_to_time: Optional[time]
    participants: Optional[List[ParticipantNode]]
    business: Optional[BusinessNode]


@strawberry.type
class EventListByDateNode:
    date: datetime
    list: List[EventNode]


@strawberry.type
class CreateEventErrorNode(ErrorNode):
    @strawberry.enum
    class CreateEventErrorCode(enum.Enum):
        NOT_CREATED = 'not_created'
        BUSINESS_NOT_EXISTS = 'business_not_exists'
        PARTICIPANT_NOT_EXISTS = 'participant_not_exists'
        PARTICIPANT_FIELDS_ARE_EMPTY = 'participants_fields_are_empty'

    code: CreateEventErrorCode


@strawberry.type
class UpdateInfoEventErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateInfoEventErrorCode(enum.Enum):
        NOT_UPDATED = 'not_updated'
        EVENT_NOT_EXISTS = 'event_not_exists'
        UPDATE_INFO_IS_EMPTY = 'update_info_is_empty'

    code: UpdateInfoEventErrorCode


@strawberry.type
class DeleteEventErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteEventErrorCode(enum.Enum):
        NOT_DELETED = 'not_deleted'
        EVENT_NOT_EXISTS = 'event_not_exists'

    code: DeleteEventErrorCode


@strawberry.type
class DeleteParticipantErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteParticipantErrorCode(enum.Enum):
        NOT_DELETED = 'not_deleted'
        PARTICIPANT_NOT_EXISTS = 'participant_not_exists'
        PARTICIPANT_DOES_NOT_BELONG_TO_YOU = 'participant_does_not_belong_to_you'


@strawberry.type
class CreateEventNode:
    created: bool
    event: Optional[EventNode]
    error: Optional[CreateEventErrorNode]


@strawberry.type
class UpdateInfoEventNode:
    updated: bool
    event: Optional[EventNode]
    error: Optional[UpdateInfoEventErrorNode]


@strawberry.type
class DeleteEventNode:
    deleted: bool
    error: Optional[DeleteEventErrorNode]


@strawberry.type
class DeleteParticipantNode:
    deleted: bool
    error: Optional[DeleteParticipantErrorNode]


@strawberry.type
class GetEventsNode:
    events: Optional[List[EventListByDateNode]]


class CreateEventData(BaseModel):
    event_name: constr(max_length=100)
    event_description: constr(max_length=1000)
    event_date: datetime
    event_from_time: Optional[time]
    event_to_time: Optional[time]
    business_id: Optional[int]
    clients_id: Optional[List[int]]


class UpdateInfoEventData(BaseModel):
    event_id: int
    event_name: constr(max_length=100)
    event_description: constr(max_length=1000)
    event_date: datetime
    event_from_time: Optional[time]
    event_to_time: Optional[time]
    business_id: Optional[int]


class DeleteEventData(BaseModel):
    event_id: int


class DeleteParticipantData(BaseModel):
    participant_id: int


class GetEventsData(BaseModel):
    from_data: Optional[datetime]
    to_data: Optional[datetime]


@strawberry.experimental.pydantic.input(model=CreateEventData, fields=[
    "event_name",
    "event_description",
    "event_date",
    "event_from_time",
    "event_to_time",
    "business_id",
    "clients_id"
])
class CreateEventInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateInfoEventData, fields=[
    "event_id",
    "event_name",
    "event_description",
    "event_date",
    "event_from_time",
    "event_to_time",
    "business_id"
])
class UpdateInfoEventInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteEventData, fields=[
    "event_id"
])
class DeleteEventInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteParticipantData, fields=[
    "participant_id",
])
class DeleteParticipantInputData:
    pass


@strawberry.experimental.pydantic.input(model=GetEventsData, fields=[
    "from_data",
    "to_data"
])
class GetEventsInputData:
    pass
