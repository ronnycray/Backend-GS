from services.authorization import AuthenticationRequiredField
from services.business.schema import (
    CreateBusinessInputData, CreateBusinessNode,
    UpdateDataBusinessInputData, UpdateDataBusinessNode,
    DeleteBusinessInputData, DeleteBusinessNode,
    CreateRoleInputData, CreateRoleNode,
    UpdateInfoRoleInputData, UpdateInfoRoleNode,
    DeleteRoleInputData, DeleteRoleNode,
    AddTeamMemberInputData, AddTeamMemberNode,
    UpdateInfoTeamMemberInputData, UpdateInfoTeamMemberNode,
    DeleteTeamMemberInputData, DeleteTeamMemberNode,
    AddClientInputData, AddClientNode,
    UpdateInfoClientInputData, UpdateInfoClientNode,
    DeleteClientInputData, DeleteClientNode,
    AddClientAttributeInputData, AddClientAttributeNode,
    UpdateInfoClientAttributeInputData, UpdateInfoClientAttributeNode,
    DeleteClientAttributeInputData, DeleteClientAttributeNode
)
from services.business.resolvers import (
    create_business_resolver,
    update_data_business_resolver,
    delete_business_resolver,
    create_role_resolver,
    update_info_role_resolver,
    delete_role_resolver,
    add_team_member_resolver,
    update_info_team_member_resolver,
    delete_team_member_resolver,
    add_client_resolver,
    update_info_client_resolver,
    delete_client_resolver,
    add_client_attribute_resolver,
    update_info_client_attribute_resolver,
    delete_client_attribute_resolver
)
from strawberry.types import Info
import strawberry


@strawberry.type
class Mutation:
    @AuthenticationRequiredField()
    async def create_business(
            self, info: Info, input_data: CreateBusinessInputData
    ) -> CreateBusinessNode:
        return await create_business_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_data_business(
            self, info: Info, input_data: UpdateDataBusinessInputData
    ) -> UpdateDataBusinessNode:
        return await update_data_business_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_business(
            self, info: Info, input_data: DeleteBusinessInputData
    ) -> DeleteBusinessNode:
        return await delete_business_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def create_role(
            self, info: Info, input_data: CreateRoleInputData
    ) -> CreateRoleNode:
        return await create_role_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_info_role(
            self, info: Info, input_data: UpdateInfoRoleInputData
    ) -> UpdateInfoRoleNode:
        return await update_info_role_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_role(
            self, info: Info, input_data: DeleteRoleInputData
    ) -> DeleteRoleNode:
        return await delete_role_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def add_team_member(
            self, info: Info, input_data: AddTeamMemberInputData
    ) -> AddTeamMemberNode:
        return await add_team_member_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_info_team_member(
            self, info: Info, input_data: UpdateInfoTeamMemberInputData
    ) -> UpdateInfoTeamMemberNode:
        return await update_info_team_member_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_team_member(
            self, info: Info, input_data: DeleteTeamMemberInputData
    ) -> DeleteTeamMemberNode:
        return await delete_team_member_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def add_client(
            self, info: Info, input_data: AddClientInputData
    ) -> AddClientNode:
        return await add_client_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_info_client(
            self, info: Info, input_data: UpdateInfoClientInputData
    ) -> UpdateInfoClientNode:
        return await update_info_client_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_client(
            self, info: Info, input_data: DeleteClientInputData
    ) -> DeleteClientNode:
        return await delete_client_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def add_client_attribute(
            self, info: Info, input_data: AddClientAttributeInputData
    ) -> AddClientAttributeNode:
        return await add_client_attribute_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_info_client_attribute(
            self, info: Info, input_data: UpdateInfoClientAttributeInputData
    ) -> UpdateInfoClientAttributeNode:
        return await update_info_client_attribute_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_client_attribute(
            self, info: Info, input_data: DeleteClientAttributeInputData
    ) -> DeleteClientAttributeNode:
        return await delete_client_attribute_resolver(info=info, input_data=input_data)
