from typing import Type, List, Optional
from sqlalchemy import select, update
from services.database import Base, BaseModel
from sqlalchemy.orm import scoped_session


def get_objects(model):
    return select(model)


async def get_objects_by_field(db: scoped_session, model: Type, field, value: str) -> List[Base]:
    statement = select(model).where(field == value)
    result = await db.execute(statement)

    return result.scalars().all()


async def get_fetchall(db: scoped_session, statement) -> list:
    result = await db.execute(statement)
    return result.fetchall()


async def delete_from_database(
        db: scoped_session, model, object_id: int
) -> bool:
    statement = select(model).where(model.id == object_id)
    result = (await db.execute(statement)).scalars().all()
    if result:
        await db.delete(result[0])
        return True
    return False


async def update_info(
        db: scoped_session, model,
        object_id: int, input_data: dict
) -> BaseModel:
    update_statement = (
        update(model)
        .where(model.id == object_id)
        .values(**input_data).returning(model)
    )

    result = await db.execute(update_statement)
    return result.fetchall()[0]


async def get_object_by_id(
        db: scoped_session, model,
        object_id: int
) -> Optional[BaseModel]:
    statement = select(model).where(model.id == object_id)
    result = (await db.execute(statement)).scalars().all()
    if result:
        return result[0]
    return None
