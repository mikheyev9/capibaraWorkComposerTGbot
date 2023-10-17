from settings.db import AsyncSessionLocal, Projects, Tasks, Users
from sqlalchemy import delete, exc


async def delete_all_data():
    async with AsyncSessionLocal() as session:
        try:
            delete_project = delete(Projects)
            delete_tasks = delete(Tasks)
            delete_users = delete(Users)
            await session.execute(delete_project)
            await session.execute(delete_tasks)
            await session.execute(delete_users)
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()


async def delete_task(task_id: str) -> None:
    async with AsyncSessionLocal() as session:
        try:
            delete_task = delete(Tasks).where(Tasks.id == task_id)
            await session.execute(delete_task)
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
