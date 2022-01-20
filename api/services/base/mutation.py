from services.base.schema import (
    RegistrationInputData,
    RegistrationNode,
    AuthenticationInputData,
    AuthenticationNode,
    ThirdPartyAuthenticationInputData,
    ThirdPartyAuthenticationNode,
    RefreshTokenInputData,
    RefreshTokenNode,
    UpdateUserInputData,
    UpdateUserNode,
    RegistrationInputData,
    RegistrationNode
)
from services.base.resolvers import (
    third_party_authentication_resolver,
    refresh_token_resolver,
    update_user_resolver,
    registration_user_resolver,
    authentication_user_resolver
)
from strawberry.types import Info
import strawberry


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def registration_user(
            self, info: Info, input_data: RegistrationInputData
    ) -> RegistrationNode:
        return await registration_user_resolver(info=info, input_data=input_data)

    @strawberry.mutation
    async def authentication_user(
            self, info: Info, input_data: AuthenticationInputData
    ) -> AuthenticationNode:
        return await authentication_user_resolver(info=info, input_data=input_data)

    @strawberry.mutation
    async def third_party_authentication(
            self, info: Info, input_data: ThirdPartyAuthenticationInputData
    ) -> ThirdPartyAuthenticationNode:
        return await third_party_authentication_resolver(info=info, input_data=input_data)

    @strawberry.mutation
    async def refresh_token(
            self, info: Info, input_data: RefreshTokenInputData
    ) -> RefreshTokenNode:
        return await refresh_token_resolver(info=info, input_data=input_data)

    @strawberry.mutation
    async def update_user(
            self, info: Info, input_data: UpdateUserInputData
    ) -> UpdateUserNode:
        return await update_user_resolver(info=info, input_data=input_data)
