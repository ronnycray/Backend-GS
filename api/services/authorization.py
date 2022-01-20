from typing import Type, Optional, Union, Awaitable, Any, Dict, List
from strawberry.field import StrawberryField
from services.base.schema import ErrorNode


class AuthenticationRequiredField(StrawberryField):
    async def get_type(self) -> Type:
        type_ = super().get_type()
        # Make sure the return type is optional
        return Optional[type_]

    async def get_result(
            self, source: Any, info: Any, args: List[Any], kwargs: Dict[str, Any]
    ) -> Union[Awaitable[Any], Any, ErrorNode]:
        if not info.context.user:
            raise ValueError(f"Token is invalid")

        return await super().get_result(args=args, source=source, info=info, kwargs=kwargs)
