from strawberry.types import Info
from services.work_with_db import (
    get_objects_by_field,
    delete_from_database,
    update_info,
    get_object_by_id
)
from services.event_calendar.schema import (
    CreateEventInputData, CreateEventNode, CreateEventErrorNode,
    UpdateInfoEventInputData, UpdateInfoEventNode, UpdateInfoEventErrorNode,
    DeleteEventInputData, DeleteEventNode, DeleteEventErrorNode,
    DeleteParticipantInputData, DeleteParticipantNode, DeleteParticipantErrorNode,
    GetEventsInputData, GetEventsNode, EventListByDateNode
)
from services.event_calendar.models import CalendarEvent, Participant
from services.business.work_with_db import (
    check_user_that_he_is_owner,
    get_client_of_user
)
from services.event_calendar.work_with_db import (
    check_event_exists,
    check_belong_participant_to_user,
    get_related_events
)


async def create_event_resolver(
        info: Info, input_data: CreateEventInputData
) -> CreateEventNode:
    instance = input_data.to_pydantic()
    context = info.context
    created = False
    event = None
    error = None

    if instance.business_id:
        user_is_owner_business = (
            await check_user_that_he_is_owner(
                db=context.db,
                user_id=context.user.id,
                business_id=instance.business_id
            )
        )
        if not user_is_owner_business:
            error = CreateEventErrorNode(
                code=CreateEventErrorNode.CreateEventErrorCode.BUSINESS_NOT_EXISTS,
                message='Business not exists or does it not belong to you'
            )

    if error is None:
        new_event = CalendarEvent(user_id=context.user.id)
        context.db.add(new_event)
        await context.db.commit()
        await update_info(
            db=context.db, model=CalendarEvent,
            object_id=new_event.id,
            input_data=instance.dict(
                exclude_unset=True, exclude_none=True,
                exclude={"clients_id"}
            )
        )

        if instance.clients_id:
            for client_id in instance.clients_id:
                user_client = await get_client_of_user(db=context.db, client_id=client_id, user_id=context.user.id)
                if user_client:
                    new_participant = Participant(
                        client_id=client_id
                    )
                    context.db.add(new_participant)
                else:
                    error = CreateEventErrorNode(
                        code=CreateEventErrorNode.CreateEventErrorCode.PARTICIPANT_NOT_EXISTS,
                        message=f"Participant with ID {client_id} not found"
                    )

        await context.db.commit()
        event = (
            await get_object_by_id(
                db=context.db,
                model=CalendarEvent,
                object_id=new_event.id
            )
        )
        created = True

    return CreateEventNode(created=created, event=event, error=error)


async def update_info_event_resolver(
        info: Info, input_data: UpdateInfoEventInputData
) -> UpdateInfoEventNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    event = None
    error = None

    event_exists = (
        await check_event_exists(
            db=context.db, user_id=context.user.id,
            event_id=instance.event_id
        )
    )

    if event_exists:
        update_data = instance.dict(
            exclude_unset=True, exclude_none=True,
            exclude={"event_id"}
        )
        if update_data:
            await update_info(
                db=context.db, model=CalendarEvent,
                object_id=instance.event_id,
                input_data=update_data
            )
            updated = True
            event = (
                await get_object_by_id(
                    db=context.db, model=CalendarEvent,
                    object_id=instance.event_id
                )
            )

        else:
            error = UpdateInfoEventErrorNode(
                code=UpdateInfoEventErrorNode.UpdateInfoEventErrorCode.UPDATE_INFO_IS_EMPTY,
                message='Update info is empty'
            )

    else:
        error = UpdateInfoEventErrorNode(
            code=UpdateInfoEventErrorNode.UpdateInfoEventErrorCode.EVENT_NOT_EXISTS,
            message='Event not found'
        )

    return UpdateInfoEventNode(updated=updated, event=event, error=error)


async def delete_event_resolver(
        info: Info, input_data: DeleteEventInputData
) -> DeleteEventNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    event_exists = (
        await check_event_exists(
            db=context.db, user_id=context.user.id,
            event_id=instance.event_id
        )
    )

    if event_exists:
        deleted = (
            await delete_from_database(
                db=context.db, model=CalendarEvent,
                object_id=instance.event_id
            )
        )
    else:
        error = DeleteEventErrorNode(
            code=DeleteEventErrorNode.DeleteEventErrorCode.EVENT_NOT_EXISTS,
            message='Event not found'
        )

    return DeleteEventNode(deleted=deleted, error=error)


async def delete_participant_resolver(
        info: Info, input_data: DeleteParticipantInputData
) -> DeleteParticipantNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    participant_exists = (
        await get_objects_by_field(
            db=context.db, model=Participant,
            field=Participant.id, value=instance.participant_id
        )
    )

    participant_does_belong_to_user = (
        await check_belong_participant_to_user(
            db=context.db, participant_id=instance.participant_id,
            user_id=info.context.user.id
        )
    )

    if participant_exists and participant_does_belong_to_user:
        deleted = (
            await delete_from_database(
                db=context.db, model=Participant,
                object_id=instance.participant_id
            )
        )

    elif not participant_exists:
        error = DeleteParticipantErrorNode(
            code=DeleteParticipantErrorNode.DeleteParticipantErrorCode.PARTICIPANT_NOT_EXISTS,
            message='Participant not exists'
        )

    elif not participant_does_belong_to_user:
        error = DeleteParticipantErrorNode(
            code=DeleteParticipantErrorNode.DeleteParticipantErrorCode.PARTICIPANT_DOES_NOT_BELONG_TO_YOU,
            message='Participant does not belong to you'
        )

    return DeleteParticipantNode(deleted=deleted, error=error)


async def get_events_resolver(
        info: Info, input_data: GetEventsInputData
) -> GetEventsNode:
    instance = input_data.to_pydantic()
    context = info.context
    events = list()
    sorting_event = dict()
    related_events = (
        await get_related_events(
            db=context.db,
            user_id=context.user.id,
            from_date=instance.from_data,
            to_date=instance.to_data
        )
    )

    for element_of_list in related_events:
        date = element_of_list.event_date.date()
        if sorting_event.get(date, None) is None:
            sorting_event[date] = list()

    for key, value in sorting_event.items():
        for element in related_events:
            if element.event_date.date() == key:
                sorting_event[key].append(
                    element
                )

    for key, value in sorting_event.items():
        events.append(
            EventListByDateNode(
                date=key,
                list=value
            )
        )

    return GetEventsNode(events=events)
