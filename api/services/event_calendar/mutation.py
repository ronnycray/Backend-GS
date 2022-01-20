from services.authorization import AuthenticationRequiredField
from services.event_calendar.schema import (
    CreateEventInputData, CreateEventNode,
    UpdateInfoEventInputData, UpdateInfoEventNode,
    DeleteEventInputData, DeleteEventNode,
    DeleteParticipantInputData, DeleteParticipantNode
)
from services.event_calendar.resolvers import (
    create_event_resolver,
    update_info_event_resolver,
    delete_event_resolver,
    delete_participant_resolver
)
from strawberry.types import Info
import strawberry


@strawberry.type
class Mutation:
    @AuthenticationRequiredField()
    async def create_event(
            self, info: Info, input_data: CreateEventInputData
    ) -> CreateEventNode:
        return await create_event_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_info_event(
            self, info: Info, input_data: UpdateInfoEventInputData
    ) -> UpdateInfoEventNode:
        return await update_info_event_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_event(
            self, info: Info, input_data: DeleteEventInputData
    ) -> DeleteEventNode:
        return await delete_event_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_participant(
            self, info: Info, input_data: DeleteParticipantInputData
    ) -> DeleteParticipantNode:
        return await delete_participant_resolver(info=info, input_data=input_data)
