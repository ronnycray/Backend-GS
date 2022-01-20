from services.authorization import AuthenticationRequiredField
import strawberry
from strawberry.types import Info
from services.event_calendar.schema import (
    GetEventsInputData, GetEventsNode
)
from services.event_calendar.resolvers import (
    get_events_resolver
)


@strawberry.type
class Query:
    @AuthenticationRequiredField()
    async def get_events(
            self, info: Info, input_data: GetEventsInputData
    ) -> GetEventsNode:
        return await get_events_resolver(info=info, input_data=input_data)
