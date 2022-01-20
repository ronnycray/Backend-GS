from strawberry.types import Info
from services.work_with_db import (
    get_objects_by_field,
    delete_from_database,
    update_info,
    get_object_by_id
)
from services.business.schema import (
    CreateBusinessInputData, CreateBusinessErrorNode, CreateBusinessNode,
    ScopedTypeNode, ClientNode,
    UpdateDataBusinessInputData, UpdateDataBusinessNode, UpdateDataBusinessErrorNode,
    DeleteBusinessInputData, DeleteBusinessNode, DeleteBusinessErrorNode,
    CreateRoleInputData, CreateRoleNode, CreateRoleErrorNode,
    UpdateInfoRoleInputData, UpdateInfoRoleNode, UpdateInfoRoleErrorNode,
    DeleteRoleInputData, DeleteRoleNode, DeleteRoleErrorNode,
    AddTeamMemberInputData, AddTeamMemberNode, AddTeamMemberErrorNode,
    UpdateInfoTeamMemberInputData, UpdateInfoTeamMemberNode, UpdateInfoTeamMemberErrorNode,
    GetBusinessTeamInputData, GetBusinessTeamNode, GetBusinessTeamErrorNode,
    DeleteTeamMemberInputData, DeleteTeamMemberNode, DeleteTeamMemberErrorNode,
    AddClientInputData, AddClientNode,
    UpdateInfoClientInputData, UpdateInfoClientNode, UpdateInfoClientErrorNode,
    DeleteClientInputData, DeleteClientNode, DeleteClientErrorNode,
    AddClientAttributeInputData, AddClientAttributeNode, AddClientAttributeErrorNode,
    UpdateInfoClientAttributeInputData, UpdateInfoClientAttributeNode, UpdateInfoClientAttributeErrorNode,
    DeleteClientAttributeInputData, DeleteClientAttributeNode, DeleteClientAttributeErrorNode
)
from services.business.models import (
    Business,
    ScopeTypeBusiness,
    BusinessRoles,
    TeamMember,
    Client,
    ClientAttribute
)
from services.base.models import (
    User
)
from services.business.work_with_db import (
    update_info_business,
    get_scoped_business_types_from_db,
    check_user_that_he_is_owner,
    check_user_that_he_is_owner_role,
    check_team_member_exists,
    get_business_team,
    client_belongs_to_user_check,
    get_clients_from_db
)
from services.base.work_with_db import (
    get_user
)
from typing import List


async def create_business_resolver(
        info: Info, input_data: CreateBusinessInputData
) -> CreateBusinessNode:
    instance = input_data.to_pydantic()
    context = info.context
    created = False
    business = None
    error = None

    scope_type_exits = (
        await get_objects_by_field(
            db=context.db, model=ScopeTypeBusiness,
            field=ScopeTypeBusiness.id, value=instance.scope_type_id
        )
    )

    if scope_type_exits:
        new_business = Business(
            user_id=context.user.id,
            scope_type_id=instance.scope_type_id,
            title=instance.title
        )
        context.db.add(new_business)
        await context.db.commit()
        await update_info_business(
            db=context.db, business_id=new_business.id,
            input_data=instance.dict(
                exclude_unset=True, exclude_none=True,
                exclude={'scope_type_id'}
            )
        )
        await context.db.commit()
        business = (
            await get_object_by_id(
                db=context.db, model=Business,
                object_id=new_business.id
            )
        )
        created = True
    else:
        error = CreateBusinessErrorNode(
            code=CreateBusinessErrorNode.CreateBusinessErrorCode.SCOPED_BUSINESS_TYPE_NOT_FOUND,
            message='Scoped business type not found'
        )

    return CreateBusinessNode(created=created, business=business, error=error)


async def get_scoped_business_types_resolver(info: Info) -> List[ScopedTypeNode]:
    context = info.context
    result = (
        await get_scoped_business_types_from_db(db=context.db)
    )

    return result


async def update_data_business_resolver(
        info: Info, input_data: UpdateDataBusinessInputData
) -> UpdateDataBusinessNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    business = None
    error = None

    user_is_owner = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            business_id=instance.business_id
        )
    )

    if user_is_owner:
        dict_input_data = instance.dict(
            exclude_unset=True, exclude_none=True,
            exclude={'business_id'}
        )
        if dict_input_data:
            business = await update_info_business(
                db=context.db, business_id=instance.business_id,
                input_data=dict_input_data
            )
            updated = True
        else:
            error = UpdateDataBusinessErrorNode(
                code=UpdateDataBusinessErrorNode.UpdateDataBusinessErrorCode.NOT_UPDATED,
                message='Not updated because empty field'
            )

    else:
        error = UpdateDataBusinessErrorNode(
            code=UpdateDataBusinessErrorNode.UpdateDataBusinessErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message='User is not owner this business'
        )

    return UpdateDataBusinessNode(updated=updated, business=business, error=error)


async def delete_business_resolver(
        info: Info, input_data: DeleteBusinessInputData
) -> DeleteBusinessNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    user_is_owner = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            business_id=instance.business_id
        )
    )

    if user_is_owner:
        deleted = (
            await delete_from_database(
                db=context.db, model=Business,
                object_id=instance.business_id
            )
        )
        if not deleted:
            error = DeleteBusinessErrorNode(
                code=DeleteBusinessErrorNode.DeleteBusinessErrorCode.NOT_DELETED,
                message='Not deleted'
            )

    else:
        error = DeleteBusinessErrorNode(
            code=DeleteBusinessErrorNode.DeleteBusinessErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message='User is not owner this business'
        )

    return DeleteBusinessNode(deleted=deleted, error=error)


async def create_role_resolver(
        info: Info, input_data: CreateRoleInputData
) -> CreateRoleNode:
    instance = input_data.to_pydantic()
    context = info.context
    created = False
    error = None
    role = None

    user_is_owner = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            business_id=instance.business_id
        )
    )

    if user_is_owner:
        new_role = BusinessRoles(
            business_id=instance.business_id
        )
        context.db.add(new_role)
        await context.db.commit()
        role = (
            await update_info(
                db=context.db, model=BusinessRoles,
                object_id=new_role.id,
                input_data=instance.dict(
                    exclude_unset=True, exclude_none=True,
                    exclude={'business_id'}
                )
            )
        )
        created = True

    else:
        error = CreateRoleErrorNode(
            code=CreateRoleErrorNode.CreateRoleErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message='User is not owner this business'
        )

    return CreateRoleNode(created=created, role=role, error=error)


async def update_info_role_resolver(
        info: Info, input_data: UpdateInfoRoleInputData
) -> UpdateInfoRoleNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    error = None
    role = None

    user_is_owner = (
        await check_user_that_he_is_owner_role(
            db=context.db,
            user_id=context.user.id,
            role_id=instance.role_id
        )
    )

    update_input_data = instance.dict(
        exclude_unset=True, exclude_none=True,
        exclude={'role_id'}
    )

    if user_is_owner and update_input_data:
        role = (
            await update_info(
                db=context.db, model=BusinessRoles,
                object_id=instance.role_id,
                input_data=update_input_data
            )
        )

    elif not update_input_data:
        error = UpdateInfoRoleErrorNode(
            code=UpdateInfoRoleErrorNode.UpdateInfoRoleErrorCode.NOT_UPDATED,
            message="Fields are empty"
        )

    elif not user_is_owner:
        error = UpdateInfoRoleErrorNode(
            code=UpdateInfoRoleErrorNode.UpdateInfoRoleErrorCode.USER_IS_NOT_OWNER_ROLE,
            message="User is not owner role"
        )

    return UpdateInfoRoleNode(updated=updated, role=role, error=error)


async def delete_role_resolver(
        info: Info, input_data: DeleteRoleInputData
) -> DeleteRoleNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    user_is_owner = (
        await check_user_that_he_is_owner_role(
            db=context.db,
            user_id=context.user.id,
            role_id=instance.role_id
        )
    )

    if user_is_owner:
        deleted = (
            await delete_from_database(
                db=context.db, model=BusinessRoles,
                object_id=instance.role_id
            )
        )

    else:
        error = DeleteRoleErrorNode(
            code=DeleteRoleErrorNode.DeleteRoleErrorCode.USER_IS_NOT_OWNER_ROLE,
            message="User is not owner role"
        )

    return DeleteRoleNode(deleted=deleted, error=error)


async def add_team_member_resolver(
        info: Info, input_data: AddTeamMemberInputData
) -> AddTeamMemberNode:
    instance = input_data.to_pydantic()
    context = info.context
    added = False
    error = None
    team_member = None
    assumed_team_member_data = {
        'user_id': None,
        'email': instance.email
    }

    user_is_owner = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            business_id=instance.business_id
        )
    )

    user_is_owner_role = (
        await check_user_that_he_is_owner_role(
            db=context.db,
            user_id=context.user.id,
            role_id=instance.role_id
        )
    )

    user_exists = (
        await get_user(
            db=context.db, field=User.email,
            value=instance.email
        )
    )

    if user_exists:
        assumed_team_member = user_exists[0]
        assumed_team_member_data["user_id"] = assumed_team_member.id
        team_member_exists = (
            await check_team_member_exists(
                db=context.db,
                team_member_id=assumed_team_member.id,
                business_id=instance.business_id
            )
        )

        if team_member_exists:
            error = AddTeamMemberErrorNode(
                code=AddTeamMemberErrorNode.AddTeamMemberErrorCode.TEAM_MEMBER_EXISTS,
                message="Team member exists yet"
            )

    if user_is_owner and user_is_owner_role and error is None:
        if assumed_team_member_data['user_id']:
            new_team_member = TeamMember(
                user_id=assumed_team_member_data['user_id'],
                email=assumed_team_member_data['email'],
                business_id=instance.business_id,
                role_id=instance.role_id
            )
        else:
            new_team_member = TeamMember(
                email=assumed_team_member_data['email'],
                business_id=instance.business_id,
                role_id=instance.role_id
            )
        context.db.add(new_team_member)
        await context.db.commit()
        instance_data = instance.dict(
            exclude_unset=True, exclude_none=True,
            exclude={'business_id', 'role_id', 'email'}
        )

        if instance_data:
            await update_info(
                db=context.db,
                model=TeamMember,
                object_id=new_team_member.id,
                input_data=instance_data
            )
        team_member = (
            await get_object_by_id(
                db=context.db,
                model=TeamMember,
                object_id=new_team_member.id
            )
        )
        added = True

    elif not user_is_owner:
        error = AddTeamMemberErrorNode(
            code=AddTeamMemberErrorNode.AddTeamMemberErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message="User is not owner business"
        )

    elif not user_is_owner_role:
        error = AddTeamMemberErrorNode(
            code=AddTeamMemberErrorNode.AddTeamMemberErrorCode.USER_IS_NOT_OWNER_ROLE,
            message="User is not owner role"
        )

    return AddTeamMemberNode(added=added, team_member=team_member, error=error)


async def update_info_team_member_resolver(
        info: Info, input_data: UpdateInfoTeamMemberInputData
) -> UpdateInfoTeamMemberNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    error = None
    team_member = None

    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            team_member_id=instance.team_member_id
        )
    )

    user_exists = True
    if instance.user_id:
        user_exists = (
            await get_user(
                db=context.db, field=User.id,
                value=instance.user_id
            )
        )

    user_is_owner_role = (
        await check_user_that_he_is_owner_role(
            db=context.db,
            user_id=context.user.id,
            team_member_id=instance.team_member_id
        )
    )

    if user_is_owner_business and user_exists and user_is_owner_role:
        instance_data = instance.dict(
            exclude_unset=True, exclude_none=True,
            exclude={'team_member_id'}
        )
        if instance_data:
            await update_info(
                db=context.db,
                model=TeamMember,
                object_id=instance.team_member_id,
                input_data=instance_data
            )
            await context.db.commit()
            team_member = (
                await get_object_by_id(
                    db=context.db,
                    model=TeamMember,
                    object_id=instance.team_member_id
                )
            )

        else:
            error = UpdateInfoTeamMemberErrorNode(
                code=UpdateInfoTeamMemberErrorNode.UpdateInfoTeamMemberErrorCode.NOT_UPDATED,
                message="Not updated because fields is empty"
            )

    elif not user_is_owner_business:
        error = UpdateInfoTeamMemberErrorNode(
            code=UpdateInfoTeamMemberErrorNode.UpdateInfoTeamMemberErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message="User is not owner business"
        )

    elif not user_exists:
        error = UpdateInfoTeamMemberErrorNode(
            code=UpdateInfoTeamMemberErrorNode.UpdateInfoTeamMemberErrorCode.USER_NOT_EXISTS,
            message="User not exists"
        )

    elif not user_is_owner_role:
        error = UpdateInfoTeamMemberErrorNode(
            code=UpdateInfoTeamMemberErrorNode.UpdateInfoTeamMemberErrorCode.USER_IS_NOT_OWNER_ROLE,
            message="User is not owner role"
        )

    return UpdateInfoTeamMemberNode(updated=updated, team_member=team_member, error=error)


async def get_business_team_resolver(
        info: Info, input_data: GetBusinessTeamInputData
) -> GetBusinessTeamNode:
    instance = input_data
    context = info.context
    error = None
    team = None

    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            business_id=instance.business_id
        )
    )

    if user_is_owner_business:
        team = (
            await get_business_team(
                db=context.db,
                business_id=instance.business_id
            )
        )
        if not team:
            error = GetBusinessTeamErrorNode(
                code=GetBusinessTeamErrorNode.GetBusinessTeamErrorCode.TEAM_IS_EMPTY,
                message='Business team is empty'
            )

    else:
        error = GetBusinessTeamErrorNode(
            code=GetBusinessTeamErrorNode.GetBusinessTeamErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message='User is not owner business'
        )

    return GetBusinessTeamNode(team=team, error=error)


async def delete_team_member_resolver(
        info: Info, input_data: DeleteTeamMemberInputData
) -> DeleteTeamMemberNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    user_is_owner_business = (
        await check_user_that_he_is_owner(
            db=context.db,
            user_id=context.user.id,
            team_member_id=instance.team_member_id
        )
    )

    if user_is_owner_business:
        deleted = (
            await delete_from_database(
                db=context.db, model=TeamMember,
                object_id=instance.team_member_id
            )
        )

    else:
        error = DeleteTeamMemberErrorNode(
            code=DeleteTeamMemberErrorNode.DeleteTeamMemberErrorCode.USER_IS_NOT_OWNER_BUSINESS,
            message='User is not owner business'
        )

    return DeleteTeamMemberNode(deleted=deleted, error=error)


async def add_client_resolver(
        info: Info, input_data: AddClientInputData
) -> AddClientNode:
    instance = input_data.to_pydantic()
    context = info.context
    error = None

    new_client = Client(
        user_id=context.user.id
    )
    context.db.add(new_client)
    await context.db.commit()
    await update_info(
        db=context.db, model=Client,
        object_id=new_client.id,
        input_data=instance.dict(
            exclude_unset=True, exclude_none=True
        )
    )
    await context.db.commit()
    client = (
        await get_objects_by_field(
            db=context.db, model=Client,
            field=Client.id, value=new_client.id
        )
    )[0]
    added = True

    return AddClientNode(added=added, client=client, error=error)


async def update_info_client_resolver(
        info: Info, input_data: UpdateInfoClientInputData
) -> UpdateInfoClientNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    client = None
    error = None

    client_exists = (
        await get_objects_by_field(
            db=context.db, model=Client,
            field=Client.id, value=instance.client_id
        )
    )

    client_belongs_to_user = (
        await client_belongs_to_user_check(
            db=context.db, user_id=context.user.id,
            client_id=instance.client_id
        )
    )

    if client_exists and client_belongs_to_user:
        update_input_data = instance.dict(
            exclude_unset=True, exclude_none=True,
            exclude={'client_id'}
        )
        if update_input_data:
            client = (
                await update_info(
                    db=context.db, model=Client,
                    object_id=instance.client_id,
                    input_data=update_input_data
                )
            )
            updated = True

        else:
            error = UpdateInfoClientErrorNode(
                code=UpdateInfoClientErrorNode.UpdateInfoClientErrorCode.CLIENT_INFO_IS_EMPTY,
                message='Client information is empty'
            )

    elif not client_exists:
        error = UpdateInfoClientErrorNode(
            code=UpdateInfoClientErrorNode.UpdateInfoClientErrorCode.CLIENT_NOT_FOUND,
            message='Client not found'
        )

    elif not client_belongs_to_user:
        error = UpdateInfoClientErrorNode(
            code=UpdateInfoClientErrorNode.UpdateInfoClientErrorCode.CLIENT_DOES_NOT_BELONG_TO_YOU,
            message='Client does not belong to you'
        )

    return UpdateInfoClientNode(updated=updated, client=client, error=error)


async def delete_client_resolver(
        info: Info, input_data: DeleteClientInputData
) -> DeleteClientNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    client_exists = (
        await get_objects_by_field(
            db=context.db, model=Client,
            field=Client.id, value=instance.client_id
        )
    )

    client_belongs_to_user = (
        await client_belongs_to_user_check(
            db=context.db, user_id=context.user.id,
            client_id=instance.client_id
        )
    )

    if client_exists and client_belongs_to_user:
        deleted = (
            await delete_from_database(
                db=context.db, model=Client,
                object_id=instance.client_id
            )
        )

    elif not client_exists:
        error = DeleteClientErrorNode(
            code=DeleteClientErrorNode.DeleteClientErrorCode.CLIENT_NOT_FOUND,
            message='Client not found'
        )

    elif not client_belongs_to_user:
        error = DeleteClientErrorNode(
            code=DeleteClientErrorNode.DeleteClientErrorNode.CLIENT_DOES_NOT_BELONG_TO_YOU,
            message='Client does not belong to you'
        )

    return DeleteClientNode(deleted=deleted, error=error)


async def add_client_attribute_resolver(
        info: Info, input_data: AddClientAttributeInputData
) -> AddClientAttributeNode:
    instance = input_data.to_pydantic()
    context = info.context
    added = False
    client = None
    error = None

    client_exists = (
        await get_objects_by_field(
            db=context.db, model=Client,
            field=Client.id, value=instance.client_id
        )
    )

    client_belongs_to_user = (
        await client_belongs_to_user_check(
            db=context.db, user_id=context.user.id,
            client_id=instance.client_id
        )
    )

    if client_exists and client_belongs_to_user:
        new_client_attribute = ClientAttribute(
            client_id=instance.client_id,
            attribute_key=instance.attribute_key,
            attribute_value=instance.attribute_value
        )
        context.db.add(new_client_attribute)
        await context.db.commit()
        client = (
            await get_object_by_id(
                db=context.db,
                model=Client,
                object_id=instance.client_id
            )
        )
        added = True

    elif not client_exists:
        error = AddClientAttributeErrorNode(
            code=AddClientAttributeErrorNode.AddClientAttributeErrorCode.CLIENT_NOT_FOUND,
            message='Client not found'
        )

    elif not client_belongs_to_user:
        error = AddClientAttributeErrorNode(
            code=AddClientAttributeErrorNode.AddClientAttributeErrorCode.CLIENT_DOES_NOT_BELONG_TO_YOU,
            message='Client does not belong to you'
        )

    return AddClientAttributeNode(added=added, client=client, error=error)


async def update_info_client_attribute_resolver(
        info: Info, input_data: UpdateInfoClientAttributeInputData
) -> UpdateInfoClientAttributeNode:
    instance = input_data.to_pydantic()
    context = info.context
    updated = False
    client = None
    error = None

    client_attribute_exists = (
        await get_objects_by_field(
            db=context.db, model=ClientAttribute,
            field=ClientAttribute.id, value=instance.client_attribute_id
        )
    )

    if client_attribute_exists:
        client_attribute = client_attribute_exists[0]
        client_belongs_to_user = (
            await client_belongs_to_user_check(
                db=context.db, user_id=context.user.id,
                client_id=client_attribute.client_id
            )
        )

        update_input_data = instance.dict(
            exclude_unset=True, exclude_none=True,
            exclude={'client_attribute_id'}
        )

        if client_belongs_to_user and update_input_data:
            await update_info(
                db=context.db, model=ClientAttribute,
                object_id=instance.client_attribute_id,
                input_data=update_input_data
            )
            await context.db.commit()
            updated = True
            client = (
                await get_object_by_id(
                    db=context.db,
                    model=Client,
                    object_id=instance.client_id
                )
            )

        elif not client_belongs_to_user:
            error = UpdateInfoClientAttributeErrorNode(
                code=UpdateInfoClientAttributeErrorNode.UpdateInfoClientAttributeErrorCode.CLIENT_DOES_NOT_BELONG_TO_YOU,
                message='Client does not belong to you'
            )

        elif not update_input_data:
            error = UpdateInfoClientAttributeErrorNode(
                code=UpdateInfoClientAttributeErrorNode.UpdateInfoClientAttributeErrorCode.CLIENT_ATTRIBUTE_IS_EMPTY,
                message='Client attribute info is empty'
            )

    else:
        error = UpdateInfoClientAttributeErrorNode(
            code=UpdateInfoClientAttributeErrorNode.UpdateInfoClientAttributeErrorCode.CLIENT_ATTRIBUTE_NOT_FOUND,
            message='Client attribute not found'
        )

    return UpdateInfoClientAttributeNode(updated=updated, client=client, error=error)


async def delete_client_attribute_resolver(
        info: Info, input_data: DeleteClientAttributeInputData
) -> DeleteClientAttributeNode:
    instance = input_data.to_pydantic()
    context = info.context
    deleted = False
    error = None

    client_attribute_exists = (
        await get_objects_by_field(
            db=context.db, model=ClientAttribute,
            field=ClientAttribute.id, value=instance.client_attribute_id
        )
    )

    if client_attribute_exists:
        client_attribute = client_attribute_exists[0]
        client_belongs_to_user = (
            await client_belongs_to_user_check(
                db=context.db, user_id=context.user.id,
                client_id=client_attribute.client_id
            )
        )

        if client_belongs_to_user:
            deleted = (
                await delete_from_database(
                    db=context.db, model=ClientAttribute,
                    object_id=instance.client_attribute_id
                )
            )

        else:
            error = DeleteClientAttributeErrorNode(
                code=DeleteClientAttributeErrorNode.DeleteClientAttributeErrorCode.CLIENT_DOES_NOT_BELONG_TO_YOU,
                message='Client does not belong to you'
            )

    else:
        error = DeleteClientAttributeErrorNode(
            code=DeleteClientAttributeErrorNode.DeleteClientAttributeErrorCode.CLIENT_ATTRIBUTE_NOT_FOUND,
            message='Client attribute not found'
        )

    return DeleteClientAttributeNode(deleted=deleted, error=error)


async def get_clients_resolver(info: Info) -> List[ClientNode]:
    context = info.context
    clients = (
        await get_clients_from_db(
            db=context.db, user_id=context.user.id
        )
    )
    return clients
