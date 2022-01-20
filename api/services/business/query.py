from services.authorization import AuthenticationRequiredField
import strawberry
from typing import List
from strawberry.types import Info
from services.business.resolvers import (
    get_scoped_business_types_resolver,
    get_business_team_resolver,
    get_clients_resolver
)
from services.business.schema import (
    ScopedTypeNode,
    GetBusinessTeamInputData, GetBusinessTeamNode,
    ClientNode
)


@strawberry.type
class Query:
    @strawberry.field
    async def get_scoped_business_types(self, info: Info) -> List[ScopedTypeNode]:
        return await get_scoped_business_types_resolver(info=info)

    @AuthenticationRequiredField()
    async def get_business_team(
            self, info: Info, input_data: GetBusinessTeamInputData
    ) -> GetBusinessTeamNode:
        return await get_business_team_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def get_clients(self, info: Info) -> List[ClientNode]:
        return await get_clients_resolver(info=info)
