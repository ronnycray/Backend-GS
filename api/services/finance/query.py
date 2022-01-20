from services.authorization import AuthenticationRequiredField
import strawberry
from strawberry.types import Info
from services.finance.schema import (
    GetHistoryTransactionsInputData, HistoryTransactionsNode,
    GetFinancialTagsInputData, FinancialTagsNode
)
from services.finance.resolvers import (
    get_history_transactions_resolver,
    get_financial_tags_resolver
)


@strawberry.type
class Query:
    @AuthenticationRequiredField()
    async def get_history_transactions(
            self, info: Info, input_data: GetHistoryTransactionsInputData
    ) -> HistoryTransactionsNode:
        return await get_history_transactions_resolver(info=info, input_data=input_data)

    @AuthenticationRequiredField()
    async def get_financial_tags(
            self, info: Info, input_data: GetFinancialTagsInputData
    ) -> FinancialTagsNode:
        return await get_financial_tags_resolver(info=info, input_data=input_data)
