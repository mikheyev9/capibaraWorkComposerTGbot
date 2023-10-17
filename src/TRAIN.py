from settings.db import AsyncSessionLocal, ChatId, Projects, ProjectsSite, Tasks, Users
from sqlalchemy import select
import asyncio

async def get_tasks_in_db(tasks_id_in_work_composer):
    async with AsyncSessionLocal() as session:
        try:
            db_task_id = await session.execute(
                select(Tasks).where(
                    Tasks.id_in_work_composer == tasks_id_in_work_composer
                )
            )
            db_task_id = db_task_id.scalars().first()
        except Exception:
            db_task_id = None
    return db_task_id

x = '648c53bbc163ea7093e9b942'
#f = get_tasks_in_db(x)
f = asyncio.run(get_tasks_in_db(x))
print(f)