from dataclasses import dataclass
from typing import Any, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Query, Session

from ...db import TradeEntity


@dataclass
class Paginator:
    page: int
    count: int


def apply_pagination(query: Query, paginator: Paginator) -> Query:
    offset = paginator.count * (paginator.page - 1)
    return query.limit(paginator.count).offset(offset)


def query_trades(session: Session, paginator: Paginator, symbol: str) -> Tuple[list[TradeEntity], Any]:
    if symbol:
        query = Query(TradeEntity).join(TradeEntity.base).filter_by(symbol=symbol)
    else:
        query = Query(TradeEntity).join(TradeEntity.base)
    query_paginated = apply_pagination(query, paginator)
    results = session.execute(query_paginated)
    total_rows = session.execute(select([func.count()]).select_from(query)).scalar()
    results = results.scalars().fetchall()
    return results, total_rows
