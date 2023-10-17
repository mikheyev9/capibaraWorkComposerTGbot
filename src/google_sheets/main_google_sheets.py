import asyncio

from crud.create_data_db import create_projects_site
from crud.read_data_db import get_projects_in_db, get_projects_site_in_db, get_users_in_db
from crud.update_data_db import update_projects_site
from google_sheets.auth_and_permissions import service_google_sheets
from google_sheets.get_cell_google_sheets import spreadsheet_read_all_values, spreadsheet_read_color_from_data
from google_sheets.parse_data_from_google_sheets import parse_all_read_data
from google_sheets.update_cell_google_sheets import (update_after_buy_domain, update_after_buy_domain_and_frontend,
                                                     update_after_content, update_after_project)
from logging_to_project import logger_to_project
from settings.config import bot
from telegram.send_message import generate_message_to_send_from_google_sheets
from work_composer.main_work_composer import create_task_from_google_sheets


async def check_all_data(json_google_sheets_all_data, service, sheetId):
    PROJECT_BACKEND = await get_projects_in_db('63c67b380ff1890d2f8e06d1')
    USER_BACKEND = await get_users_in_db('6426b18b4a953d04136382db')
    PROJECT_PARSING = await get_projects_in_db('63c7606a0ff1890d2f4d0d77')
    USER_PARSING = await get_users_in_db('63ce92bc2a23703765836236')

    try:
        values_list = json_google_sheets_all_data.values
    except AttributeError:
        return None

    for value in values_list:
        row = value.row
        project_site_data = value.dict()

        project_site = await get_projects_site_in_db(value.project)

        if project_site is not None and row != project_site.row:
            project_site_data = project_site.__dict__
            project_site_data['row'] = row
            await update_projects_site(project_site.id, project_site_data)

        project_site_data['is_complite'] = False
        if project_site is None:
            project_site_data['create_project'] = None
            project_site_data['parsing'] = None
            project_site_data['verstka'] = None
            project_site_data['buy_domain'] = None
            project_site_data['content'] = None
            project_site_data['deploy'] = None
            project_site_data['acquiring'] = None
            project_site_data['release'] = None
            project_site = await create_projects_site(project_site_data)
            await update_after_project(row)

            message_to_send = f'Появился новый проект {value.project}'
            await generate_message_to_send_from_google_sheets(bot, message_to_send)
            title = f'[Сайты] "{value.project}" Создание проекта'
            description = ''
            await create_task_from_google_sheets(
                title,
                description,
                user=USER_BACKEND,
                project=PROJECT_BACKEND,
                project_site=project_site,
                tags='@r1kk1s'
            )
            title = f'[Сайты] "{value.project}" Парсинг'
            description = ''
            await create_task_from_google_sheets(
                title,
                description,
                user=USER_PARSING,
                project=PROJECT_PARSING,
                project_site=project_site,
                tags='@nik_tere'
            )
        elif project_site.is_complite is True:
            continue

        if project_site.buy_domain == '' or project_site.buy_domain is None:
            if value.buy_domain is None or value.buy_domain == '':
                continue
            elif value.buy_domain != '':
                project_site_data['buy_domain'] = value.buy_domain
                project_site_data['verstka'] = project_site.verstka
                project_site_data['parsing'] = project_site.parsing
                project_site_data['create_project'] = project_site.create_project
                await update_projects_site(project_site.id, project_site_data)
                await update_after_buy_domain(row)
                message_to_send = f'[Сайты] "{value.project}" появился домен {value.buy_domain}'
                await generate_message_to_send_from_google_sheets(bot, message_to_send)
                if project_site.verstka == 'True':
                    title = f'[Сайты] "{value.project}" Установка на домен "{value.buy_domain}"'
                    description = ''
                    await create_task_from_google_sheets(
                        title,
                        description,
                        user=USER_BACKEND,
                        project=PROJECT_BACKEND,
                        project_site=project_site,
                        tags='@r1kk1s'
                    )
                    await update_after_buy_domain_and_frontend(row)

        if project_site.content == '' or project_site.content is None:
            color_cell = await spreadsheet_read_color_from_data(service_google_sheets, ranges=[f'G{row}'])
            if_green_color_sell = [
                color_cell['red'] == 0.20392157,
                color_cell['blue'] == 0.3254902,
                color_cell['green'] == 0.65882355
            ]
            if all(if_green_color_sell):
                project_site_data['deploy'] = project_site.deploy
                project_site_data['verstka'] = project_site.verstka
                project_site_data['content'] = 'True'
                project_site_data['parsing'] = project_site.parsing
                project_site_data['buy_domain'] = value.buy_domain
                project_site_data['create_project'] = project_site.create_project
                await update_after_content(row)
                await update_projects_site(project_site.id, project_site_data)
                title = f'[Сайты] "{value.project}" Подключение эквайринга на "{value.buy_domain}"'
                description = ''
                await create_task_from_google_sheets(
                    title,
                    description,
                    user=USER_BACKEND,
                    project=PROJECT_BACKEND,
                    project_site=project_site,
                    tags='@r1kk1s'
                )
                message_to_send = f'[Сайты] "{value.project}" контент готов'
                await generate_message_to_send_from_google_sheets(bot, message_to_send)


async def main_google_sheets():
    import time
    sheetId = '1065963106'
    while True:
        start_time = time.time()
        try:
            response = await spreadsheet_read_all_values(service_google_sheets, 'I')
            json_google_sheets_all_data = await parse_all_read_data(response)
            await check_all_data(json_google_sheets_all_data, service_google_sheets, sheetId)
        except Exception:
            logger_to_project.exception('Exception')
        logger_to_project.info(f'google sheet was worked {time.time() - start_time} sec')

        await asyncio.sleep(120)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main_google_sheets())
