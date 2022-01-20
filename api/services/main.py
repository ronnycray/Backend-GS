import logging

from starlette.responses import Response, HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.websockets import WebSocket
from starlette.requests import Request
from starlette.routing import Route

from typing import NamedTuple, Optional, Union, AsyncGenerator

from strawberry import field, mutation, subscription
from strawberry import Schema
from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.asgi.handlers import HTTPHandler
from strawberry.types import ExecutionResult
from strawberry import type as type_strawberry

from sqlalchemy.ext.asyncio import AsyncSession

from services.database import get_db
from services.base.models import User
from services.base.work_with_db import get_user

from services.base.mutation import Mutation as MutationBase
from services.business.mutation import Mutation as MutationBusiness
from services.event_calendar.mutation import Mutation as MutationEventCalendar
from services.finance.mutation import Mutation as MutationFinance

from services.base.query import Query as QueryBase
from services.business.query import Query as QueryBusiness
from services.event_calendar.query import Query as QueryEventCalendar
from services.finance.query import Query as QueryFinance

from services.config import get_settings

import asyncio
import pathlib
import time
import jwt

# from services.settings_db.filling import filling_database_default_values


class Context(NamedTuple):
    """
    Context object that is attached to a strawberry
    `Info` instance and passed to resolvers.
    """
    request: Optional[Union[Request, WebSocket]]
    response: Optional[Response]
    db: Optional[AsyncSession]
    user: Optional[User] = None


def get_graphiql_html() -> str:
    here = pathlib.Path(__file__).parents[1]
    logging.warning(f'HERE: {here=}')
    path = here / "static/graphiql.html"
    logging.warning(f'NEW HERE: {here=}')

    with open(path) as f:
        template = f.read()
        logging.warning(template)

    return template


class CustomHTTPHandler(HTTPHandler):
    async def execute(
            self, query, variables=None, context: Optional[Context] = None,
            operation_name=None, root_value=None
    ) -> ExecutionResult:
        logging.warning(F"EXECUTE")
        """
        Overwriting the `execute` method so that we call field
        resolvers and mutations when a Sentry user scope is pushed.
        This is also a good place
        to close the db session.
        """
        # TODO: maybe add other misc processing
        result = None
        try:
            result = await super().execute(
                query, variables=variables, context=context,
                operation_name=operation_name, root_value=root_value
            )
            if context and context.db and result.errors is None:
                logging.warning(f'CONTEXT COMMIT')
                # Commit session that was opened in `GraphQL.get_context`
                await context.db.commit()
        except Exception as e:
            logging.warning(f"Execute error: {e}")
            await context.db.rollback()
        finally:
            if context and context.db and result.errors is None:
                logging.warning(f'CONTEXT COMMIT')
                # Close session that was opened in `GraphQL.get_context`
                await context.db.rollback()
            await context.db.close()
            logging.warning('Session is closed')
        return result


class GraphQL(BaseGraphQL):
    http_handler_class = CustomHTTPHandler

    async def get_context(
            self, request: Union[Request, WebSocket],
            response: Optional[Response] = None
    ) -> Context:
        """
        Create a context instance with the db and
        TODO: lazily load currently authenticated user
        so that all resolvers and mutations have access to a db session
        and the user instance.
        """
        logging.warning(F"CONTEXT START")
        user = None

        headers = request.headers
        token_is_present = headers.get('authorization', False)
        if token_is_present:
            db = get_db()
            jwt_setting = get_settings()
            jwt_token = token_is_present.replace('JWT ', '')
            try:
                decode_token = jwt.decode(jwt_token, jwt_setting.secret_key, algorithms=[jwt_setting.algorithm])
                expire_jwt_token = decode_token.get('exp', False)
                email = decode_token.get('email', False)
                now = time.time()
                required_parameters_are_correct = all(
                    (
                        email, expire_jwt_token, (now <= expire_jwt_token)
                    )
                )
                logging.warning(f"{decode_token=}")
                if required_parameters_are_correct:
                    user_instance = await get_user(db=db, field=User.email, value=email)
                    if user_instance:
                        user = user_instance[0]
            except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as jwt_error:
                logging.warning(jwt_error)
                await db.rollback()

            await db.close()

        cnt = Context(
            request=request,
            response=response,
            db=get_db(),
            user=user
        )
        return cnt


@type_strawberry()
class Query(
    QueryBase,
    QueryBusiness,
    QueryEventCalendar,
    QueryFinance
):
    @field
    async def check(self) -> bool:
        return True


@type_strawberry()
class Mutation(
    MutationBase,
    MutationBusiness,
    MutationEventCalendar,
    MutationFinance
):
    @mutation
    async def check(self) -> bool:
        return True


@type_strawberry
class Subscription:
    @subscription
    async def check(self) -> AsyncGenerator[bool, None]:
        try:
            while True:
                yield True
                await asyncio.sleep(2)
        except Exception as e:
            logging.warning(f"{e=}")


graphql_app = GraphQL(
    schema=Schema(query=Query, mutation=Mutation, subscription=Subscription)
)

routes = [
    Route('/graphql', graphql_app)
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_headers=['*'],
        allow_methods=("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"),
    )
]

app = Starlette(
    routes=routes,
    on_startup=[
        # filling_database_default_values
    ],
    on_shutdown=[],
    middleware=middleware
)

app.add_websocket_route("/graphql", graphql_app)
