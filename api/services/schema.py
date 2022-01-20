from enum import Enum

import strawberry


@strawberry.type
class ErrorNode:
    message: str
    code: str
