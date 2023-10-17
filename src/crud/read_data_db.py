from settings.db import AsyncSessionLocal, ChatId, Projects, ProjectsSite, Tasks, Users
from sqlalchemy import select


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


async def get_tasks_by_id_project_site_in_db(projects_site_id):
    async with AsyncSessionLocal() as session:
        db_task = await session.execute(
            select(Tasks).where(
                Tasks.id_project_site == str(projects_site_id)
            )
        )
        db_task = db_task.scalars().all()
    return db_task


async def get_projects_site_in_db(projects_site_project):
    async with AsyncSessionLocal() as session:
        db_project_id = await session.execute(
            select(ProjectsSite).where(
                ProjectsSite.project == projects_site_project
            )
        )
        db_project_id = db_project_id.scalars().first()
    return db_project_id


async def get_projects_site_by_id_in_db(projects_site_id):
    async with AsyncSessionLocal() as session:
        db_project_id = await session.execute(
            select(ProjectsSite).where(
                ProjectsSite.id == projects_site_id
            )
        )
        db_project_id = db_project_id.scalars().first()
    return db_project_id


async def get_projects_in_db(project_id_in_work_composer):
    async with AsyncSessionLocal() as session:
        db_project_id = await session.execute(
            select(Projects).where(
                Projects.id_in_work_composer == project_id_in_work_composer
            )
        )
        db_project_id = db_project_id.scalars().first()
    return db_project_id


async def get_users_in_db(users_id_in_work_composer):
    async with AsyncSessionLocal() as session:
        db_users_id = await session.execute(
            select(Users).where(
                Users.id_in_work_composer == users_id_in_work_composer
            )
        )
        db_users_id = db_users_id.scalars().first()
    return db_users_id


async def get_all_chat_id():
    async with AsyncSessionLocal() as session:
        db_chat_id = await session.execute(select(ChatId))
        db_chat_id = db_chat_id.all()
    return db_chat_id
