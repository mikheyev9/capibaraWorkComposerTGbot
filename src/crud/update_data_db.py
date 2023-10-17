from settings.db import AsyncSessionLocal, ProjectsSite, Tasks
from sqlalchemy import exc, update


async def update_projects_site(project_id, data):
    async with AsyncSessionLocal() as session:
        try:
            update_data = (
                update(
                    ProjectsSite
                    ).where(
                        ProjectsSite.id == int(project_id)
                    ).values(
                        is_complite=data['is_complite'],
                        row=data['row'],
                        project=data['project'],
                        create_project=data['create_project'],
                        parsing=data['parsing'],
                        verstka=data['verstka'],
                        buy_domain=data['buy_domain'],
                        deploy=data['deploy'],
                        content=data['content'],
                        acquiring=data['acquiring'],
                        release=data['release'],
                    )
            )
            await session.execute(update_data)
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
        else:
            return True


async def update_task(id_in_work_composer, data):
    async with AsyncSessionLocal() as session:
        try:
            update_data = (
                update(
                    Tasks
                    ).where(
                        Tasks.id_in_work_composer == id_in_work_composer
                    ).values(
                        title=data.get('title'),
                        description=data.get('description'),
                        id_users=data.get('id_users'),
                        status=data.get('status')
                    )
            )
            await session.execute(update_data)
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
        else:
            return True
