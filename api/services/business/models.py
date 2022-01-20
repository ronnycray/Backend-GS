from sqlalchemy import (
    Column, Integer, ForeignKey, VARCHAR, Boolean,
    String, Enum, TIMESTAMP, Float
)
from sqlalchemy.orm import relationship
from services.database import BaseModel
from datetime import datetime
from services.business.enums import (
    BusinessStatus, RolePrivileges, MemberType, UserTypeForBusiness, StatusUserForBusiness
)
from services.event_calendar.models import Participant


class ScopeTypeBusiness(BaseModel):
    """
    All existing types of scope businesses in the system are listed here
    """
    __tablename__ = 'scope_type_business'
    __tableargs__ = {
        'comment': "Table for description of scope type business"
    }

    name = Column(VARCHAR(255), nullable=False, default="")
    description = Column(String(3000), nullable=False, default="")
    hide = Column(Boolean, default=False)

    def __repr__(self):
        return f"Business: {self.name} | Hide status: {self.hide}"


class Business(BaseModel):
    __tablename__ = 'business'
    __tableargs__ = {
        'comment': "Table of user businesses"
    }

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )
    title = Column(VARCHAR(255), nullable=False, default="")
    scope_type_id = Column(
        Integer,
        ForeignKey('scope_type_business.id', ondelete='SET DEFAULT'),
        default=1
    )
    type_business = Column(
        Enum(UserTypeForBusiness, native_enum=False),
        nullable=False,
        default=UserTypeForBusiness.INDIVIDUAL
    )
    status_business = Column(
        Enum(BusinessStatus, native_enum=False),
        nullable=False,
        default=BusinessStatus.NOT_ACTIVE
    )
    registration_date = Column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
    description = Column(VARCHAR(4000), nullable=False, default="")
    address = Column(VARCHAR(255), nullable=False, default="")
    services = Column(VARCHAR(4000), nullable=False, default="")
    region = Column(VARCHAR(255), nullable=False, default="")
    city = Column(VARCHAR(255), nullable=False, default="")
    latitude = Column(Float(precision=20), nullable=False, default=0)
    longitude = Column(Float(precision=20), nullable=False, default=0)
    email = Column(VARCHAR(255), nullable=False, default="")
    phone = Column(VARCHAR(255), nullable=False, default="")
    website = Column(VARCHAR(255), nullable=False, default="")
    operation_hours = Column(VARCHAR(255), nullable=False, default="")
    # TODO: make field logo picture from depot or aws
    logo_picture = Column(VARCHAR(255), nullable=False, default="")

    owner = relationship("User", lazy='selectin', foreign_keys=[user_id], back_populates="businesses")
    roles = relationship("BusinessRoles", lazy='selectin')
    scoped_type = relationship("ScopeTypeBusiness", lazy='selectin', foreign_keys=[scope_type_id], uselist=False)
    teams = relationship("TeamMember", lazy='selectin')
    events = relationship("CalendarEvent", lazy='selectin', back_populates="business", uselist=True)
    # financial_account = relationship("FinancialBusiness", lazy='selectin', back_populates="business", uselist=False)

    def __repr__(self):
        return f'UserID: {self.user_id} | Business: {self.title}'


class BusinessRoles(BaseModel):
    __tablename__ = 'business_roles'
    __tableargs__ = {
        'comment': "Table of business roles"
    }

    business_id = Column(Integer, ForeignKey('business.id', ondelete='CASCADE'))
    name = Column(VARCHAR(255), nullable=False, default="")
    description = Column(VARCHAR(4000), nullable=False, default="")

    business = relationship("Business", lazy='selectin', foreign_keys=[business_id], back_populates="roles")
    role_permissions = relationship("RolePermissions", lazy='selectin')

    def __repr__(self):
        return f"Business Role: {self.name} | ID: {self.id} | Business ID: {self.business_id}"


class RolePermissions(BaseModel):
    __tablename__ = 'role_permissions'
    __tableargs__ = {
        'comment': "Table permissions of business roles"
    }

    role_id = Column(Integer, ForeignKey('business_roles.id', ondelete='CASCADE'))
    full_access = Column(
        Enum(RolePrivileges, native_enum=False),
        nullable=False,
        default=RolePrivileges.READ_ONLY
    )


class TeamMember(BaseModel):
    __tablename__ = 'team_member'
    __tableargs__ = {
        'comment': "Table of team business members"
    }

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )
    business_id = Column(
        Integer,
        ForeignKey('business.id', ondelete='CASCADE')
    )
    role_id = Column(
        Integer,
        ForeignKey('business_roles.id', ondelete='CASCADE')
    )
    email = Column(
        VARCHAR(255),
        nullable=False,
        default=""
    )
    date_from = Column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
    date_to = Column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
    description = Column(VARCHAR(4000), nullable=False, default="")
    member_type = Column(
        Enum(MemberType, native_enum=False),
        nullable=False,
        default=MemberType.STAFF
    )
    member_status = Column(Boolean, default=False)

    member = relationship("User", lazy='selectin', foreign_keys=[user_id], back_populates="teams_member")
    business = relationship("Business", lazy='selectin', foreign_keys=[business_id], back_populates="teams")
    role = relationship("BusinessRoles", lazy='selectin', foreign_keys=[role_id])

    def __repr__(self):
        return f"Member of team business ID: {self.business_id} | UserID: {self.user_id}"


class Client(BaseModel):
    __tablename__ = 'client'
    __tableargs__ = {
        'comment': "Business owner's clients Table"
    }

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )
    name = Column(VARCHAR(255), nullable=False, default="")
    user_type = Column(
        Enum(UserTypeForBusiness, native_enum=False),
        nullable=False,
        default=UserTypeForBusiness.INDIVIDUAL
    )
    status = Column(
        Enum(StatusUserForBusiness, native_enum=False),
        nullable=False,
        default=StatusUserForBusiness.NEW
    )
    region = Column(VARCHAR(255), nullable=False, default="")
    city = Column(VARCHAR(255), nullable=False, default="")
    address = Column(VARCHAR(255), nullable=False, default="")
    email = Column(VARCHAR(255), nullable=False, default="")
    phone = Column(VARCHAR(255), nullable=False, default="")
    latitude = Column(Float(precision=20), nullable=False, default=0)
    longitude = Column(Float(precision=20), nullable=False, default=0)
    client_user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )
    description = Column(VARCHAR(4000), nullable=False, default="")
    birthday = Column(TIMESTAMP, nullable=False, default=datetime.now())

    attributes = relationship("ClientAttribute", lazy='selectin', foreign_keys='[ClientAttribute.client_id]')
    owner = relationship("User", lazy='selectin', foreign_keys=[user_id], back_populates="clients")
    events = relationship("Participant", lazy='selectin', foreign_keys='[Participant.client_id]', uselist=True)

    def __repr__(self):
        return f"Client user ID: {self.client_user_id} of UserID: {self.user_id}"


class ClientAttribute(BaseModel):
    __tablename__ = 'client_attribute'
    __tableargs__ = {
        'comment': "Client attribute parameters of user"
    }

    client_id = Column(
        Integer,
        ForeignKey('client.id', ondelete='CASCADE')
    )
    attribute_key = Column(VARCHAR(255), nullable=False, default="")
    attribute_value = Column(VARCHAR(255), nullable=False, default="")

    client = relationship("Client", lazy='selectin', foreign_keys=[client_id], back_populates="attributes")

    def __repr__(self):
        return f"Client user ID: {self.client_user_id} attribute: {self.attribute_key}: {self.attribute_value}"
