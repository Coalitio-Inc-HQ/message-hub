from src.database import session_factory
from sqlalchemy import text

import asyncio

async def test():
    async with session_factory() as session:
        res = await session.execute(text("Select 1"))
        print(res.all())
asyncio.run(test())