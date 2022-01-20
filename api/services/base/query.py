from services.authorization import AuthenticationRequiredField
import strawberry
from services.base.schema import (
    GetMeNode
)
from strawberry.types import Info
from services.base.resolvers import get_me_resolver


@strawberry.type
class Query:
    @AuthenticationRequiredField()
    async def get_me(self, info: Info) -> GetMeNode:
        return await get_me_resolver(info=info)
