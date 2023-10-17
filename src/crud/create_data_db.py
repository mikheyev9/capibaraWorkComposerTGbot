from settings.db import AsyncSessionLocal, ChatId, Projects, ProjectsSite, Tasks, Users
from sqlalchemy import exc


async def create_projects_site(new_projects_site):
    db_project = ProjectsSite(**new_projects_site)

    async with AsyncSessionLocal() as session:
        try:
            session.add(db_project)
            await session.commit()
            await session.refresh(db_project)
        except exc.IntegrityError:
            await session.rollback()
        else:
            return db_project


async def create_projects(new_project_data):
    db_project = Projects(**new_project_data)

    async with AsyncSessionLocal() as session:
        try:
            session.add(db_project)
            await session.commit()
            await session.refresh(db_project)
        except exc.IntegrityError:
            await session.rollback()
        else:
            return db_project


async def create_tasks(new_tasks_data):
    db_tasks = Tasks(**new_tasks_data)

    async with AsyncSessionLocal() as session:
        try:
            session.add(db_tasks)
            await session.commit()
            await session.refresh(db_tasks)
        except exc.IntegrityError:
            await session.rollback()
        else:
            return db_tasks


async def create_users(new_users_data):
    db_users = Users(**new_users_data)

    async with AsyncSessionLocal() as session:
        try:
            session.add(db_users)
            await session.commit()
            await session.refresh(db_users)
        except exc.IntegrityError:
            await session.rollback()
        else:
            return db_users


async def create_chat_id(new_chat_id_data):
    db_chat_id = ChatId(**new_chat_id_data)

    async with AsyncSessionLocal() as session:
        try:
            session.add(db_chat_id)
            await session.commit()
            await session.refresh(db_chat_id)
        except exc.IntegrityError:
            await session.rollback()
        else:
            return db_chat_id
