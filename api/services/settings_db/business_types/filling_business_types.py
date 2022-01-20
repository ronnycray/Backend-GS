from sqlalchemy import select, insert
from services.database import get_db
from services.business.models import ScopeTypeBusiness
import json

with open('services/settings_db/business_types/types.json', 'r', encoding='utf-8') as lib:
    data = json.load(lib)


async def filling_business_type():
    db = get_db()
    for element in data['types']:
        statement = select(ScopeTypeBusiness).where(
            ScopeTypeBusiness.name == element['name']
        )
        result = (await db.execute(statement)).scalars().all()
        print('result', result)
        if not result:
            new_type = ScopeTypeBusiness(
                name=element['name'],
                description=element['description']
            )
            db.add(new_type)

    await db.commit()
    await db.close()
