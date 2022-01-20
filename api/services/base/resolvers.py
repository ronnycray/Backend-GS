from strawberry.types import Info
from services.work_with_db import get_objects_by_field
from sqlalchemy.orm import scoped_session
from services.base.schema import (
    RegistrationInputData,
    RegistrationNode,
    RegistrationError,
    AuthenticationInputData,
    AuthenticationNode,
    AuthenticationError,
    ThirdPartyAuthenticationInputData,
    ThirdPartyAuthenticationNode,
    ThirdPartyAuthenticationError,
    RefreshTokenInputData,
    RefreshTokenError,
    RefreshTokenNode,
    GetMeNode,
    UpdateUserInputData,
    UpdateUserNode,
    UpdateUserError,
    RegistrationInputData,
    RegistrationNode,
    RegistrationError
)
from services.base.models import (
    User,
    ThirdPartyAuthentication,
    RefreshToken
)
from services.base.work_with_db import (
    add_user,
    get_user,
    refresh_token_exists,
    create_refresh_token,
    update_refresh_token,
    update_user_info,
    update_device_of_user,
    fill_in_related_services_by_user
)
from services.config import get_settings
from datetime import datetime, timedelta
from time import mktime
import secrets
import jwt


def get_access_token(email: str) -> str:
    jwt_setting = get_settings()
    exp_token = datetime.now() + timedelta(minutes=jwt_setting.access_token_expire_minutes)
    payload = {
        "email": email,
        "exp": mktime(exp_token.timetuple())
    }
    token = jwt.encode(payload=payload, key=jwt_setting.secret_key,
                       algorithm=jwt_setting.algorithm)

    return token


async def generate_refresh_token(db: scoped_session) -> str:
    jwt_setting = get_settings()
    token_refresh = secrets.token_hex(nbytes=jwt_setting.bytes_refresh_token)

    while await refresh_token_exists(db=db, token=token_refresh):
        token_refresh = secrets.token_hex(nbytes=jwt_setting.bytes_refresh_token)

    return token_refresh


async def registration_user_resolver(
        info: Info, input_data: RegistrationInputData
) -> RegistrationNode:
    instance = input_data.to_pydantic()
    context = info.context
    success = False
    user = None
    error = None
    token = None
    token_refresh = None

    email_is_already_taken = (
        await get_objects_by_field(
            db=context.db, model=User,
            field=User.email, value=instance.email
        )
    )
    if not email_is_already_taken:
        user = User(email=instance.email, password=instance.password)
        context.db.add(user)
        await context.db.commit()

        success = True

        new_data = reform_third_party_input_data_to_dict(instance=instance,
                                                         exclude={'email', 'password', 'uid', 'device_id'})

        if new_data:
            await update_user_info(
                db=context.db,
                user=user,
                instance=new_data
            )
            await context.db.commit()

        third_party_object = ThirdPartyAuthentication(
            user_id=user.id, google_uid=instance.uid
        )
        context.db.add(third_party_object)
        await context.db.commit()

        await update_device_of_user(
            db=context.db,
            user=user,
            device_id=instance.device_id
        )

        await fill_in_related_services_by_user(db=context.db, user=user)

        token_refresh = await generate_refresh_token(db=context.db)
        await create_refresh_token(
            db=context.db,
            user_id=user.id,
            refresh_token=token_refresh
        )
        token = get_access_token(email=user.email)

        # activate_code = await create_email_code(db=context.db, user_id=user.id, model=ActivateCode)
        # await context.db.commit()
        # result = await send_email(email=user.email, subject=mail_text.subject_activate_code,
        #                           message_str=mail_text.text_activate_code.format(activate_code),
        #                           message_html=mail_text.text_activate_code.format(activate_code))
        # if result:
        #     code_sent = True

    elif email_is_already_taken:
        error = RegistrationError(
            code=RegistrationError.RegistrationErrorCode.EMAIL_TAKEN,
            message="Email is taken",
        )

    return RegistrationNode(
        token=token, token_refresh=token_refresh,
        user=user, registration_success=success, error=error
    )


async def authentication_user_resolver(
        info: Info, input_data: AuthenticationInputData
) -> AuthenticationNode:
    instance = input_data.to_pydantic()
    context = info.context
    auth_success = False
    token = None
    token_refresh = None
    error = None

    user = (
        await get_user(
            db=context.db, field=User.email,
            value=instance.email
        )
    )

    if user:
        user = user[0]
        if user.password == instance.password:
            token_refresh = await generate_refresh_token(db=context.db)
            await create_refresh_token(
                db=context.db,
                user_id=user.id,
                refresh_token=token_refresh
            )
            token = get_access_token(email=user.email)
            auth_success = True

        else:
            error = AuthenticationError(
                code=AuthenticationError.AuthenticationErrorCode.WRONG_CREDENTIALS,
                message="Wrong credentials",
            )

    else:
        error = AuthenticationError(
            code=AuthenticationError.AuthenticationErrorCode.WRONG_CREDENTIALS,
            message="Wrong credentials",
        )

    return AuthenticationNode(authentication_status=auth_success, token=token,
                              token_refresh=token_refresh, error=error)


async def create_access_tokens(db: scoped_session, user: User):
    token_refresh = await generate_refresh_token(db=db)
    await create_refresh_token(
        db=db,
        user_id=user.id,
        refresh_token=token_refresh
    )
    token = get_access_token(email=user.email)

    return token_refresh, token


def reform_third_party_input_data_to_dict(instance: ThirdPartyAuthenticationInputData,
                                          exclude: set = None) -> dict:
    if exclude is None:
        exclude = {'uid', 'display_name', 'device_id'}
    new_data = instance.dict(exclude_unset=True, exclude_none=True, exclude=exclude)
    if instance.display_name:
        first_name = instance.display_name.split(' ')[0]
        second_name = instance.display_name.split(' ')[1]
        new_data['first_name'] = first_name
        new_data['second_name'] = second_name

    return new_data


async def third_party_authentication_resolver(
        info: Info, input_data: ThirdPartyAuthenticationInputData
) -> ThirdPartyAuthenticationNode:
    instance = input_data.to_pydantic()
    context = info.context
    status = False
    token = None
    token_refresh = None
    error = None

    user = (
        await get_user(
            db=context.db, field=User.email,
            value=instance.email
        )
    )

    uid_is_already_taken = (
        await get_objects_by_field(
            db=context.db, model=ThirdPartyAuthentication,
            field=ThirdPartyAuthentication.google_uid,
            value=instance.uid
        )
    )

    if user:
        user = user[0]

        if user.credentials.google_uid == instance.uid:
            token_refresh, token = await create_access_tokens(db=context.db, user=user)
            new_data = reform_third_party_input_data_to_dict(instance=instance)

            await update_user_info(
                db=context.db,
                user=user,
                instance=new_data
            )
            await update_device_of_user(
                db=context.db,
                user=user,
                device_id=instance.device_id
            )

            status = True

        else:
            error = ThirdPartyAuthenticationError(
                code=ThirdPartyAuthenticationError.ThirdPartyAuthenticationErrorCode.WRONG_CREDENTIALS,
                message="Wrong credentials",
            )
    else:
        if not uid_is_already_taken:
            new_data = reform_third_party_input_data_to_dict(instance=instance)

            user = await add_user(db=context.db, instance=new_data)
            await context.db.commit()

            third_party_object = ThirdPartyAuthentication(
                user_id=user.id, google_uid=instance.uid
            )
            context.db.add(third_party_object)
            await context.db.commit()

            await update_device_of_user(
                db=context.db,
                user=user,
                device_id=instance.device_id
            )

            await fill_in_related_services_by_user(db=context.db, user=user)
            token_refresh, token = await create_access_tokens(db=context.db, user=user)
            status = True

        else:
            error = ThirdPartyAuthenticationError(
                code=ThirdPartyAuthenticationError.ThirdPartyAuthenticationErrorCode.UID_EXISTS,
                message="UID exists",
            )

    return ThirdPartyAuthenticationNode(status=status, token=token, token_refresh=token_refresh, error=error)


async def refresh_token_resolver(info: Info, input_data: RefreshTokenInputData) -> RefreshTokenNode:
    instance = input_data.to_pydantic()
    context = info.context
    access_token = None
    refresh_token_str = None
    error = None
    token_is_already = await get_objects_by_field(
        db=context.db, model=RefreshToken,
        field=RefreshToken.refresh_token, value=instance.token
    )
    if token_is_already:
        object_token = token_is_already[0]
        now = datetime.now()
        if now <= object_token.expires_at:
            refresh_token_str = await generate_refresh_token(db=context.db)
            user = await get_objects_by_field(db=context.db, model=User, field=User.id,
                                              value=object_token.user_id)
            user = user[0]
            refresh_token_object = await update_refresh_token(db=context.db,
                                                              id_token=object_token.id,
                                                              new_refresh_token=refresh_token_str)
            refresh_token_str = refresh_token_object.refresh_token
            access_token = get_access_token(email=user.email)
        else:
            error = RefreshTokenError(
                code=RefreshTokenError.RefreshTokenErrorCode.EXPIRED,
                message="Refresh token expired",
            )
    else:
        error = RefreshTokenError(
            code=RefreshTokenError.RefreshTokenErrorCode.INVALID,
            message="Refresh token is invalid",
        )

    return RefreshTokenNode(error=error, access_token=access_token, refresh_token=refresh_token_str)


async def get_me_resolver(info: Info) -> GetMeNode:
    user = info.context.user
    return GetMeNode(user=user, error=None)


async def update_user_resolver(
        info: Info, input_data: UpdateUserInputData
) -> UpdateUserNode:
    instance = input_data.to_pydantic().dict(exclude_unset=True, exclude_none=True)
    context = info.context
    updated = False
    user = None
    error = None

    if instance:
        user = (
            await update_user_info(
                db=context.db,
                user=context.user,
                instance=instance
            )
        )
        updated = True
    else:
        error = UpdateUserError(
            code=UpdateUserError.UpdateUserErrorCode.EMPTY_FIELDS,
            message='All fields is empty'
        )

    return UpdateUserNode(user=user, updated=updated, error=error)
