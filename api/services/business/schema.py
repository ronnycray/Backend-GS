import enum
from typing import Optional, List

from services.config import get_settings

import strawberry
from services.schema import ErrorNode
from pydantic import BaseModel, constr, EmailStr
from datetime import datetime
from services.business.enums import UserTypeForBusiness, MemberType
from services.finance.schema import FinanceAccount


settings = get_settings()


@strawberry.type
class ScopedTypeNode:
    id: int
    name: str
    description: str


@strawberry.type
class RoleNode:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str]


@strawberry.type
class MemberNode:
    email: str
    first_name: str
    second_name: str
    middle_name: str
    phone: str
    birthday: datetime
    profile_picture: Optional[str]


@strawberry.type
class ClientAttributeNode:
    id: int
    attribute_key: str
    attribute_value: str


@strawberry.type
class ClientNode:
    id: int
    name: str
    region: Optional[str]
    city: Optional[str]
    address: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    client_user_id: Optional[int]
    description: Optional[str]
    birthday: Optional[datetime]
    attributes: Optional[List[ClientAttributeNode]]


@strawberry.type
class TeamMember:
    id: int
    role: RoleNode
    member_type: MemberType
    member_status: bool
    email: Optional[str]
    member: Optional[MemberNode]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    description: Optional[str]


@strawberry.type
class BusinessNode:
    id: int
    title: str
    scoped_type: ScopedTypeNode
    created_at: datetime
    updated_at: datetime
    description: Optional[str]
    address: Optional[str]
    services: Optional[str]
    region: Optional[str]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    type_business: Optional[UserTypeForBusiness]
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    operation_hours: Optional[str]
    roles: Optional[List[RoleNode]]
    teams: Optional[List[TeamMember]]


@strawberry.type
class CreateBusinessErrorNode(ErrorNode):
    @strawberry.enum
    class CreateBusinessErrorCode(enum.Enum):
        NOT_CREATED = 'not_created'
        SCOPED_BUSINESS_TYPE_NOT_FOUND = 'scoped_business_type_not_found'

    code: CreateBusinessErrorCode


@strawberry.type
class UpdateDataBusinessErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateDataBusinessErrorCode(enum.Enum):
        NOT_UPDATED = 'not_updated'
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'

    code: UpdateDataBusinessErrorCode


@strawberry.type
class DeleteBusinessErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteBusinessErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'
        NOT_DELETED = 'not_deleted'

    code: DeleteBusinessErrorCode


@strawberry.type
class CreateRoleErrorNode(ErrorNode):
    @strawberry.enum
    class CreateRoleErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'
        NOT_CREATED = 'not_created'

    code: CreateRoleErrorCode


@strawberry.type
class UpdateInfoRoleErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateInfoRoleErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_ROLE = 'user_is_not_owner_role'
        NOT_UPDATED = 'not_updated'

    code: UpdateInfoRoleErrorCode


@strawberry.type
class DeleteRoleErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteRoleErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_ROLE = 'user_is_not_owner_role'

    code: DeleteRoleErrorCode


@strawberry.type
class AddTeamMemberErrorNode(ErrorNode):
    @strawberry.enum
    class AddTeamMemberErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'
        TEAM_MEMBER_EXISTS = 'team_member_exists'
        USER_IS_NOT_OWNER_ROLE = 'user_is_not_owner_role'
        USER_NOT_EXISTS = 'user_not_exists'

    code: AddTeamMemberErrorCode


@strawberry.type
class UpdateInfoTeamMemberErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateInfoTeamMemberErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'
        TEAM_MEMBER_EXISTS = 'team_member_exists'
        USER_IS_NOT_OWNER_ROLE = 'user_is_not_owner_role'
        USER_NOT_EXISTS = 'user_not_exists'
        MEMBER_HAVE_ROLE = 'member_have_role'
        NOT_UPDATED = 'not_updated'

    code: UpdateInfoTeamMemberErrorCode


@strawberry.type
class GetBusinessTeamErrorNode(ErrorNode):
    @strawberry.enum
    class GetBusinessTeamErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'
        TEAM_IS_EMPTY = 'team_is_empty'

    code: GetBusinessTeamErrorCode


@strawberry.type
class DeleteTeamMemberErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteTeamMemberErrorCode(enum.Enum):
        USER_IS_NOT_OWNER_BUSINESS = 'user_is_not_owner_business'
        MEMBER_NOT_EXISTS = 'member_not_exists'

    code: DeleteTeamMemberErrorCode


@strawberry.type
class AddClientErrorNode(ErrorNode):
    @strawberry.enum
    class AddClientErrorCode(enum.Enum):
        NOT_ADDED_CLIENT = 'not_added_client'

    code: AddClientErrorCode


@strawberry.type
class UpdateInfoClientErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateInfoClientErrorCode(enum.Enum):
        CLIENT_DOES_NOT_BELONG_TO_YOU = 'client_does_not_belong_to_you'
        CLIENT_NOT_FOUND = 'client_not_found'
        CLIENT_INFO_IS_EMPTY = 'client_info_is_empty'

    code: UpdateInfoClientErrorCode


@strawberry.type
class DeleteClientErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteClientErrorCode(enum.Enum):
        CLIENT_DOES_NOT_BELONG_TO_YOU = 'client_does_not_belong_to_you'
        CLIENT_NOT_FOUND = 'client_not_found'

    code: DeleteClientErrorCode


@strawberry.type
class AddClientAttributeErrorNode(ErrorNode):
    @strawberry.enum
    class AddClientAttributeErrorCode(enum.Enum):
        CLIENT_DOES_NOT_BELONG_TO_YOU = 'client_does_not_belong_to_you'
        CLIENT_NOT_FOUND = 'client_not_found'

    code: AddClientAttributeErrorCode


@strawberry.type
class UpdateInfoClientAttributeErrorNode(ErrorNode):
    @strawberry.enum
    class UpdateInfoClientAttributeErrorCode(enum.Enum):
        CLIENT_DOES_NOT_BELONG_TO_YOU = 'client_does_not_belong_to_you'
        CLIENT_NOT_FOUND = 'client_not_found'
        CLIENT_ATTRIBUTE_NOT_FOUND = 'client_attribute_not_found'
        CLIENT_ATTRIBUTE_IS_EMPTY = 'client_attribute_is_empty'

    code: UpdateInfoClientAttributeErrorCode


@strawberry.type
class DeleteClientAttributeErrorNode(ErrorNode):
    @strawberry.enum
    class DeleteClientAttributeErrorCode(enum.Enum):
        CLIENT_DOES_NOT_BELONG_TO_YOU = 'client_does_not_belong_to_you'
        CLIENT_NOT_FOUND = 'client_not_found'
        CLIENT_ATTRIBUTE_NOT_FOUND = 'client_attribute_not_found'

    code: DeleteClientAttributeErrorCode


@strawberry.type
class CreateBusinessNode:
    created: bool
    business: Optional[BusinessNode]
    error: Optional[CreateBusinessErrorNode]


@strawberry.type
class UpdateDataBusinessNode:
    updated: bool
    business: Optional[BusinessNode]
    error: Optional[UpdateDataBusinessErrorNode]


@strawberry.type
class DeleteBusinessNode:
    deleted: bool
    error: Optional[DeleteBusinessErrorNode]


@strawberry.type
class CreateRoleNode:
    created: bool
    role: Optional[RoleNode]
    error: Optional[CreateRoleErrorNode]


@strawberry.type
class UpdateInfoRoleNode:
    updated: bool
    role: Optional[RoleNode]
    error: Optional[UpdateInfoRoleErrorNode]


@strawberry.type
class DeleteRoleNode:
    deleted: bool
    error: Optional[DeleteRoleErrorNode]


@strawberry.type
class AddTeamMemberNode:
    added: bool
    team_member: Optional[TeamMember]
    error: Optional[AddTeamMemberErrorNode]


@strawberry.type
class UpdateInfoTeamMemberNode:
    updated: bool
    team_member: Optional[TeamMember]
    error: Optional[UpdateInfoTeamMemberErrorNode]


@strawberry.type
class GetBusinessTeamNode:
    team: Optional[List[TeamMember]]
    error: Optional[GetBusinessTeamErrorNode]


@strawberry.type
class DeleteTeamMemberNode:
    deleted: bool
    error: Optional[DeleteTeamMemberErrorNode]


@strawberry.type
class AddClientNode:
    added: bool
    client: Optional[ClientNode]
    error: Optional[AddClientErrorNode]


@strawberry.type
class UpdateInfoClientNode:
    updated: bool
    client: Optional[ClientNode]
    error: Optional[UpdateInfoClientErrorNode]


@strawberry.type
class DeleteClientNode:
    deleted: bool
    error: Optional[DeleteClientErrorNode]


@strawberry.type
class AddClientAttributeNode:
    added: bool
    client: Optional[ClientNode]
    error: Optional[AddClientAttributeErrorNode]


@strawberry.type
class UpdateInfoClientAttributeNode:
    updated: bool
    client: Optional[ClientNode]
    error: Optional[UpdateInfoClientAttributeErrorNode]


@strawberry.type
class DeleteClientAttributeNode:
    deleted: bool
    error: Optional[DeleteClientAttributeErrorNode]


class CreateBusinessData(BaseModel):
    title: constr(max_length=50)
    scope_type_id: int
    type_business: Optional[UserTypeForBusiness]
    description: Optional[constr(max_length=4000)]
    address: Optional[constr(max_length=300)]
    services: Optional[constr(max_length=4000)]
    region: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    latitude: Optional[float]
    longitude: Optional[float]
    email: Optional[EmailStr]
    phone: Optional[constr(max_length=15)]
    website: Optional[constr(max_length=50)]
    operation_hours: Optional[constr(max_length=50)]


class UpdateDataBusinessData(BaseModel):
    business_id: int
    title: Optional[constr(max_length=50)]
    scope_type_id: Optional[int]
    type_business: Optional[UserTypeForBusiness]
    description: Optional[constr(max_length=4000)]
    address: Optional[constr(max_length=300)]
    services: Optional[constr(max_length=4000)]
    region: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    latitude: Optional[float]
    longitude: Optional[float]
    email: Optional[EmailStr]
    phone: Optional[constr(max_length=15)]
    website: Optional[constr(max_length=50)]
    operation_hours: Optional[constr(max_length=50)]


class DeleteBusinessData(BaseModel):
    business_id: int


class CreateRoleData(BaseModel):
    business_id: int
    name: constr(max_length=50)
    description: Optional[constr(max_length=500)]


class UpdateInfoRoleData(BaseModel):
    role_id: int
    name: Optional[constr(max_length=50)]
    description: Optional[constr(max_length=500)]


class DeleteRoleData(BaseModel):
    role_id: int


class AddTeamMemberData(BaseModel):
    email: EmailStr
    business_id: int
    role_id: int
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    description: Optional[constr(max_length=500)]


class UpdateInfoTeamMemberData(BaseModel):
    team_member_id: int
    user_id: Optional[int]
    role_id: Optional[int]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    description: Optional[constr(max_length=500)]


class DeleteTeamMemberData(BaseModel):
    team_member_id: int


class AddClientData(BaseModel):
    name: constr(max_length=50)
    region: Optional[constr(max_length=50)]
    city: Optional[constr(max_length=50)]
    address: Optional[constr(max_length=100)]
    email: Optional[EmailStr]
    phone: Optional[constr(max_length=20)]
    latitude: Optional[float]
    longitude: Optional[float]
    client_user_id: Optional[int]
    description: Optional[constr(max_length=500)]
    birthday: Optional[datetime]


class UpdateInfoClientData(BaseModel):
    client_id: int
    name: Optional[constr(max_length=50)]
    region: Optional[constr(max_length=50)]
    city: Optional[constr(max_length=50)]
    address: Optional[constr(max_length=100)]
    email: Optional[EmailStr]
    phone: Optional[constr(max_length=20)]
    latitude: Optional[float]
    longitude: Optional[float]
    client_user_id: Optional[int]
    description: Optional[constr(max_length=500)]
    birthday: Optional[datetime]


class DeleteClientData(BaseModel):
    client_id: int


class AddClientAttributeData(BaseModel):
    client_id: int
    attribute_key: constr(max_length=50)
    attribute_value: constr(max_length=100)


class UpdateInfoClientAttributeData(BaseModel):
    client_attribute_id: int
    attribute_key: Optional[constr(max_length=50)]
    attribute_value: Optional[constr(max_length=100)]


class DeleteClientAttributeData(BaseModel):
    client_attribute_id: int


@strawberry.experimental.pydantic.input(model=CreateBusinessData, fields=[
    "title",
    "scope_type_id",
    "type_business",
    "description",
    "address",
    "services",
    "region",
    "city",
    "latitude",
    "longitude",
    "email",
    "phone",
    "website",
    "operation_hours"
])
class CreateBusinessInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateDataBusinessData, fields=[
    "business_id",
    "title",
    "scope_type_id",
    "type_business",
    "description",
    "address",
    "services",
    "region",
    "city",
    "latitude",
    "longitude",
    "email",
    "phone",
    "website",
    "operation_hours"
])
class UpdateDataBusinessInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteBusinessData, fields=[
    "business_id"
])
class DeleteBusinessInputData:
    pass


@strawberry.experimental.pydantic.input(model=CreateRoleData, fields=[
    "business_id",
    "name",
    "description"
])
class CreateRoleInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateInfoRoleData, fields=[
    "role_id",
    "name",
    "description"
])
class UpdateInfoRoleInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteRoleData, fields=[
    "role_id"
])
class DeleteRoleInputData:
    pass


@strawberry.experimental.pydantic.input(model=AddTeamMemberData, fields=[
    "email",
    "business_id",
    "role_id",
    "date_from",
    "date_to",
    "description",
])
class AddTeamMemberInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateInfoTeamMemberData, fields=[
    "team_member_id",
    "user_id",
    "role_id",
    "date_from",
    "date_to",
    "description"
])
class UpdateInfoTeamMemberInputData:
    pass


@strawberry.input
class GetBusinessTeamInputData:
    business_id: int


@strawberry.experimental.pydantic.input(model=DeleteTeamMemberData, fields=[
    "team_member_id"
])
class DeleteTeamMemberInputData:
    pass


@strawberry.experimental.pydantic.input(model=AddClientData, fields=[
    "name",
    "region",
    "city",
    "address",
    "email",
    "phone",
    "latitude",
    "longitude",
    "client_user_id",
    "description",
    "birthday"
])
class AddClientInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateInfoClientData, fields=[
    "client_id",
    "name",
    "region",
    "city",
    "address",
    "email",
    "phone",
    "latitude",
    "longitude",
    "client_user_id",
    "description",
    "birthday"
])
class UpdateInfoClientInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteClientData, fields=[
    "client_id"
])
class DeleteClientInputData:
    pass


@strawberry.experimental.pydantic.input(model=AddClientAttributeData, fields=[
    "client_id",
    "attribute_key",
    "attribute_value"
])
class AddClientAttributeInputData:
    pass


@strawberry.experimental.pydantic.input(model=UpdateInfoClientAttributeData, fields=[
    "client_attribute_id",
    "attribute_key",
    "attribute_value"
])
class UpdateInfoClientAttributeInputData:
    pass


@strawberry.experimental.pydantic.input(model=DeleteClientAttributeData, fields=[
    "client_attribute_id"
])
class DeleteClientAttributeInputData:
    pass
