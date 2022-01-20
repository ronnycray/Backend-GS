from services.authorization import AuthenticationRequiredField
from services.finance.schema import (
    CreateMoneyMovementInputData, CreateMoneyMovementNode,
    CreateFinancialTagInputData, CreateFinancialTagNode,
    UpdateFinancialTagInputData, UpdateFinancialTagNode,
    DeleteFinancialTagInputData, DeleteFinancialTagNode
)
from services.finance.resolvers import (
    create_money_movement_resolver,
    create_financial_tag_resolver,
    update_financial_tag_resolver,
    delete_financial_tag_resolver
)
from strawberry.types import Info
import strawberry


@strawberry.type
class Mutation:
    @AuthenticationRequiredField()
    async def create_money_movement(
            self, info: Info, input_data: CreateMoneyMovementInputData
    ) -> CreateMoneyMovementNode:
        return await create_money_movement_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def create_financial_tag(
            self, info: Info, input_data: CreateFinancialTagInputData
    ) -> CreateFinancialTagNode:
        return await create_financial_tag_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def update_financial_tag(
            self, info: Info, input_data: UpdateFinancialTagInputData
    ) -> UpdateFinancialTagNode:
        return await update_financial_tag_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def delete_financial_tag(
            self, info: Info, input_data: DeleteFinancialTagInputData
    ) -> DeleteFinancialTagNode:
        return await delete_financial_tag_resolver(info=info, input_data=input_data)
