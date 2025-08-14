import math
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from sqlalchemy import Select, func, select, delete as sqla_delete
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = [
    "PaginatedResult",
    "paginate",
    "fetch_one",
    "fetch_all",
    "count",
    "save_one",
    "delete_one",
]

T = TypeVar("T")


@dataclass(kw_only=True)
class PaginatedResult(Generic[T]):
    has_more: bool
    total: int
    offset: int
    limit: int | None
    items: list[T]
    total_pages: int
    current_page: int


async def paginate(
    session: AsyncSession,
    statement: Select[tuple[T]],
    offset: int = 0,
    limit: int | None = None,
) -> PaginatedResult[T]:
    total = await count(session=session, statement=statement)
    statement = statement.offset(offset)
    if limit is not None:
        statement = statement.limit(limit + 1)
    results = await fetch_all(session=session, statement=statement)
    has_more = limit is not None and len(results) > limit
    return PaginatedResult(
        has_more=has_more,
        total=total or 0,
        limit=limit,
        offset=offset,
        items=list(results[:-1]) if has_more else list(results),
        total_pages=math.ceil((total - 1) / limit) + 1 if limit else 1,
        current_page=math.ceil((offset - 1) / limit) + 1 if limit else 1,
    )


async def count(session: AsyncSession, statement: Select[tuple[T]]) -> int: 
    result = await session.execute(
        select(func.count()).select_from(statement.alias())
    )
    return result.scalar() or 0


async def fetch_one(session: AsyncSession, statement: Select[tuple[T]]) -> T | None:
    result = await session.execute(statement)
    return result.scalar()


async def fetch_all(session: AsyncSession, statement: Select[tuple[T]]) -> list[T]:
    result = await session.execute(statement)
    return list(result.scalars().all())

async def save_one(session: AsyncSession, instance: T) -> T:
    session.add(instance)
    await session.commit()
    return instance

async def delete_one(session: AsyncSession, instance: Any) -> None:
    await session.delete(instance)
    await session.commit()