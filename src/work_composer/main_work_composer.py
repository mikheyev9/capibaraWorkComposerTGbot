import asyncio

from crud.create_data_db import create_projects, create_tasks, create_users
from crud.delete_data_db import delete_all_data, delete_task
from crud.read_data_db import (get_projects_in_db, get_projects_site_by_id_in_db, get_tasks_by_id_project_site_in_db,
                               get_tasks_in_db, get_users_in_db)
from crud.update_data_db import update_projects_site, update_task
# from google_sheets.update_cell_google_sheets import (update_after_buy_domain_and_frontend, update_color_acquiring,
#                                                      update_color_after_acquiring, update_color_after_create_project,
#                                                      update_color_after_deploy, update_color_after_deploy_and_parsing,
#                                                      update_color_after_frontend, update_color_after_parsing,
#                                                      update_color_after_release, update_color_correction_acquiring,
#                                                      update_color_correction_after_acquiring,
#                                                      update_color_correction_after_create_project,
#                                                      update_color_correction_after_deploy,
#                                                      update_color_correction_after_frontend,
#                                                      update_color_correction_after_parsing,
#                                                      update_color_correction_create_project,
#                                                      update_color_correction_deploy, update_color_correction_frontend,
#                                                      update_color_correction_parsing, update_color_create_project,
#                                                      update_color_deploy, update_color_frontend, update_color_parsing,
#                                                      update_color_release, update_text_in_cell)
# from google_sheets.update_rows import update_rows_for_projects_sites
from logging_to_project import logger_to_project
from settings.config import bot
from telegram.send_message import (generate_message_to_send_from_google_sheets,
                                   generate_message_to_send_from_work_composer)
from work_composer.bot_work_composer import wcsession
# from work_composer.delete_requests_to_api import delete_task_in_work_composer
# from work_composer.get_requests_to_api import (get_projects_from_work_composer, get_task_from_work_composer,
#                                                get_users_from_work_composer)
# from work_composer.post_requests_to_api import create_task_in_work_composer


async def create_and_update_task_from_work_composer(if_reset=None, project_site=None, tags=None):
    #await update_rows_for_projects_sites()
    json_data = wcsession.get_task_from_work_composer()

    skip_project_name = None
    task_to_update = []
    new_task_after_reset = []
    all_task = json_data.get('tasks')
    for task in all_task:
        id_in_work_composer = task.get('_id')
        id_projects = task.get('_project')
        id_users = task.get('_assignedTo')
        title = task.get('title')
        description = task.get('description')
        author = task.get('_author')
        status = task.get('status')

        if skip_project_name is not None and '[Сайты]' in title and skip_project_name in title:
            continue

        data = {
            'id_in_work_composer': id_in_work_composer,
            'id_projects': id_projects,
            'id_users': id_users,
            'title': title,
            'description': description,
            'author': author,
            'status': status,
            'id_project_site': ''
        }
        if project_site is not None and '[Сайты]' in title and project_site.project in title:
            data['id_project_site'] = project_site.id

        new_task = await get_tasks_in_db(id_in_work_composer)
        if new_task is not None:
            if_change_task = [
                new_task.status != status,
                new_task.id_users != id_users,
                new_task.title != title,
                new_task.description != description
            ]
            if any(if_change_task):
                logger_to_project.info(f'{new_task.title} is update with {data = }')
                new_update_task = await update_task(id_in_work_composer, data)
                if new_update_task:
                    # if new_task.id_project_site != '':
                    #     skip_project_name = await update_google_sheets_from_work_composer(
                    #         new_task,
                    #         id_projects,
                    #         description,
                    #         id_users,
                    #         data
                    #     )
                    task_to_update.append((new_task, data))
        else:
            new_task = await create_tasks(data)
            if if_reset is None and new_task:
                new_task_after_reset.append((new_task, tags))
                logger_to_project.info(f'new_task {new_task}')
                continue

    return task_to_update, new_task_after_reset


async def update_google_sheets_from_work_composer(new_task, id_projects, description, id_users, update_data):
    project_site = await get_projects_site_by_id_in_db(new_task.id_project_site)
    if project_site.is_complite is True:
        return

    project_backend = await get_projects_in_db('63c67b380ff1890d2f8e06d1')
    user_backend = await get_users_in_db('6426b18b4a953d04136382db')
    project_frontend = await get_projects_in_db('63c63f4a5ad3d206689795a0')
    user_frontend = None
    user_frontend_main = await get_users_in_db('63c6789940d01004f86970c6')

    skip_project_name = None
    data_to_update = {
        'row': project_site.row,
        'is_complite': project_site.is_complite,
        'project': project_site.project,
        'create_project': project_site.create_project,
        'parsing': project_site.parsing,
        'verstka': project_site.verstka,
        'buy_domain': project_site.buy_domain,
        'deploy': project_site.deploy,
        'content': project_site.content,
        'acquiring': project_site.acquiring,
        'release': project_site.release,
    }

    if id_projects == '63c67b380ff1890d2f8e06d1':
        if 'Создание проекта' in new_task.title:
            if update_data['status'] == 'Done' and \
                    (data_to_update['create_project'] == '' or data_to_update['create_project'] is None):
                data_to_update['create_project'] = 'True'
                title = f'[Сайты] "{project_site.project}" Редизайн'
                description = ''
                await create_task_from_google_sheets(
                    title,
                    description,
                    user=user_frontend,
                    project=project_frontend,
                    project_site=project_site,
                    tags='@Popib, @Aleksei_Pronin13'
                )
                message_to_send = (
                    f'[Сайты] "{project_site.project}" Создан проект "{project_site.project}" '
                    'нужно купить домен и текст на главню'
                    '\n@Александр'
                )
                await generate_message_to_send_from_google_sheets(bot, message_to_send)
                await update_color_after_create_project(project_site.row)
            elif update_data['status'] == 'In Progress':
                if data_to_update['create_project'] != 'True':
                    data_to_update['create_project'] = ''
                    await update_color_correction_create_project(project_site.row)
                else:
                    await update_color_create_project(project_site.row)
            elif update_data['status'] == 'Done':
                await update_color_correction_after_create_project(project_site.row)
        elif 'Установка на домен' in new_task.title:
            if update_data['status'] == 'Done' and\
                    (data_to_update['deploy'] == '' or data_to_update['deploy'] is None):
                data_to_update['deploy'] = 'True'
                await update_color_after_deploy(project_site.row)
                if data_to_update['parsing'] == 'True':
                    message_to_send = (
                        f'[Сайты] "{project_site.project}" нужен контент для {project_site.buy_domain}'
                        '\n@Александр'
                    )
                    await generate_message_to_send_from_google_sheets(bot, message_to_send)
                    await update_color_after_deploy_and_parsing(project_site.row)
            elif update_data['status'] == 'In Progress':
                if data_to_update['deploy'] != 'True':
                    data_to_update['deploy'] = ''
                    await update_color_correction_deploy(project_site.row)
                else:
                    await update_color_deploy(project_site.row)
            elif update_data['status'] == 'Done':
                await update_color_correction_after_deploy(project_site.row)
        elif 'Подключение эквайринга на' in new_task.title:
            if update_data['status'] == 'Done' and\
                    (data_to_update['acquiring'] == '' or data_to_update['acquiring'] is None):
                data_to_update['acquiring'] = 'True'
                await update_color_after_acquiring(project_site.row)
                title = f'[Сайты] "{project_site.project}" Проверить готовность проекта'
                description = ''
                await create_task_from_google_sheets(
                    title,
                    description,
                    user=user_frontend_main,
                    project=project_frontend,
                    project_site=project_site,
                    tags='@Шамиль'
                )
            elif update_data['status'] == 'In Progress':
                if data_to_update['acquiring'] != 'True':
                    data_to_update['acquiring'] = ''
                    await update_color_correction_acquiring(project_site.row)
                else:
                    await update_color_acquiring(project_site.row)
            elif update_data['status'] == 'Done':
                await update_color_correction_after_acquiring(project_site.row)
    elif id_projects == '63c63f4a5ad3d206689795a0':
        if 'Редизайн' in new_task.title:
            if update_data['status'] == 'Done' and\
                    (data_to_update['verstka'] == '' or data_to_update['verstka'] is None):
                data_to_update['verstka'] = 'True'
                await update_color_after_frontend(project_site.row)
                user_to_text = await get_users_in_db(id_users)
                if user_to_text is not None:
                    text = user_to_text.fio
                else:
                    text = 'None'
                range_cell = f'D{project_site.row}'
                await update_text_in_cell(range_cell, text)
                if data_to_update['buy_domain'] != '' or data_to_update['buy_domain'] is not None:
                    title = f'[Сайты] "{project_site.project}" Установка на домен "{project_site.buy_domain}"'
                    description = ''
                    await create_task_from_google_sheets(
                        title,
                        description,
                        user=user_backend,
                        project=project_backend,
                        project_site=project_site,
                        tags='@r1kk1s'
                    )
                    await update_after_buy_domain_and_frontend(project_site.row)
            elif update_data['status'] == 'In Progress':
                if data_to_update['verstka'] != 'True':
                    data_to_update['verstka'] = ''
                    await update_color_correction_frontend(project_site.row)
                else:
                    await update_color_frontend(project_site.row)
                if id_users is not None and id_users != '':
                    text = await get_users_in_db(id_users)
                    text = text.fio
                    range_cell = f'D{project_site.row}'
                    await update_text_in_cell(range_cell, text)
            elif update_data['status'] == 'Done':
                await update_color_correction_after_frontend(project_site.row)
                if id_users is not None and id_users != '':
                    text = await get_users_in_db(id_users)
                    text = text.fio
                    range_cell = f'D{project_site.row}'
                    await update_text_in_cell(range_cell, text)
        elif 'Проверить готовность проекта' in new_task.title:
            if update_data['status'] == 'Done' and\
                    (data_to_update['release'] == '' or data_to_update['release'] is None):
                data_to_update['is_complite'] = True
                data_to_update['release'] = 'True'
                await update_color_after_release(project_site.row)
                message_to_send = (
                    f'[Сайты] "{project_site.project}" Проект полностью готов'
                    '\n@mikes_2, @Visage228, @nuuulllllll, @DNDKINGMASTER'
                )
                await generate_message_to_send_from_google_sheets(bot, message_to_send)
                await delete_tasks_for_project_site(project_site)
                skip_project_name = project_site.project
            elif update_data['status'] == 'In Progress':
                if data_to_update['release'] != 'True':
                    data_to_update['release'] = ''
                await update_color_release(project_site.row)
    elif id_projects == '63c7606a0ff1890d2f4d0d77':
        if update_data['status'] == 'Done' and (data_to_update['parsing'] == '' or data_to_update['parsing'] is None):
            data_to_update['parsing'] = 'True'
            await update_color_after_parsing(project_site.row)
            text = description
            range_cell = f'C{project_site.row}'
            await update_text_in_cell(range_cell, text)
            if data_to_update['deploy'] == 'True':
                message_to_send = (
                    f'[Сайты] "{project_site.project}" нужен контент для {project_site.buy_domain}'
                    '\n@Александр'
                )
                await generate_message_to_send_from_google_sheets(bot, message_to_send)
                await update_color_after_deploy_and_parsing(project_site.row)
        elif update_data['status'] == 'In Progress':
            if data_to_update['parsing'] != 'True':
                data_to_update['parsing'] = ''
                await update_color_correction_parsing(project_site.row)
            else:
                await update_color_parsing(project_site.row)
            text = description
            range_cell = f'C{project_site.row}'
            await update_text_in_cell(range_cell, text)
        elif update_data['status'] == 'Done':
            text = description
            range_cell = f'C{project_site.row}'
            await update_text_in_cell(range_cell, text)
            await update_color_correction_after_parsing(project_site.row)

    await update_projects_site(project_site.id, data_to_update)
    return skip_project_name


async def create_task_from_google_sheets(title, description, user, project, project_site, tags=None):
    wcsession.create_task_in_work_composer(title, description, user, project)

    data = await create_and_update_task_from_work_composer(project_site=project_site, tags=tags)
    task_to_update, new_task_after_reset = data
    if task_to_update or new_task_after_reset:
        await generate_message_to_send_from_work_composer(bot, task_to_update, new_task_after_reset)


async def delete_tasks_for_project_site(project_site):
    tasks_for_delete = await get_tasks_by_id_project_site_in_db(project_site.id)
    if len(tasks_for_delete) != 6:
        logger_to_project.error(f'ERROR count task for delete wrong {len(tasks_for_delete) = }')
        return
    for task in tasks_for_delete:
        wcsession.delete_task_in_work_composer(task.id_in_work_composer)
        await delete_task(task.id)


async def create_projects_from_work_composer():
    json_data = wcsession.get_projects_from_work_composer()
    all_project = json_data.get('projects')
    for project in all_project:
        id_in_work_composer = project.get('_id')
        title = project.get('title')
        new_project = await create_projects(
            {
                'id_in_work_composer': id_in_work_composer,
                'title': title
            }
        )
        if new_project is None:
            new_project = await get_projects_in_db(id_in_work_composer)
        # print(new_project)


async def create_users_from_work_composer():
    json_data = wcsession.get_users_from_work_composer()
    all_users = json_data.get('users')
    for user in all_users:
        id_in_work_composer = user.get('_id')
        firstName = user.get('firstName')
        lastName = user.get('lastName')
        new_user = await create_users(
            {
                'id_in_work_composer': id_in_work_composer,
                'fio': firstName + ' ' + lastName
            }
        )
        if new_user is None:
            new_user = await get_users_in_db(id_in_work_composer)
        # print(new_user)


async def reset_data_in_db():
    await delete_all_data()
    await create_projects_from_work_composer()
    await create_users_from_work_composer()
    _ = await create_and_update_task_from_work_composer(if_reset=True)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(reset_data_in_db())
