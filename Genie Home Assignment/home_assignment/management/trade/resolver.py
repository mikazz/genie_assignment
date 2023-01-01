import strawberry

from ...deps import GenieInfo
from ..scalars import ArrowType
from .database import Paginator, query_trades


@strawberry.type
class LabelValueType:
    key: str
    value: str


@strawberry.type
class Trade:
    amount: float
    price: float
    placed_at: ArrowType
    symbol: str
    quote: str
    labels: list[LabelValueType]


@strawberry.type
class Response:
    trades: list[Trade]
    total_rows: int


async def get_trades(info: GenieInfo, page: int, count: int, symbol: str) -> Response:
    with info.context.session_factory.begin() as session:
        trades, total_rows = query_trades(session, Paginator(page=page, count=count), symbol)
        return Response(
            trades=[
                Trade(
                    amount=trade.amount,
                    price=trade.price,
                    placed_at=trade.placed_at,
                    symbol=trade.base.symbol,
                    quote=trade.quote.symbol,
                    labels=[LabelValueType(key=i.key.name, value=i.value) for i in trade.labels],
                )
                for trade in trades
            ],
            total_rows=total_rows,
        )
