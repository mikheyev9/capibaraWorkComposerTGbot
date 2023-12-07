from crud.read_data_db import get_projects_in_db, get_users_in_db


async def formatting_new_task(new_task, tags):
    author = await get_users_in_db(new_task.author)
    provision = False
    if new_task.id_projects == '655bed959f10a5e5a81baeb8':
        provision = True
    if author is None:
        str_author = 'не указан'
    else:
        str_author = author.fio

    user = await get_users_in_db(new_task.id_users)
    if user is None:
        str_user = 'не указан'
    else:
        str_user = user.fio

    project = await get_projects_in_db(new_task.id_projects)
    if project is None:
        str_project = 'не указан'
    else:
        str_project = project.title

    if new_task.description is None or new_task.description == '':
        str_description = 'не указанно'
    else:
        str_description = new_task.description

    message_to_send = (
        f'<b>{str_author}</b> создал новую задачу\n'
        f'<b>"{new_task.title}"</b>\n'
        f'в проекте <b>{str_project}</b>\n'
        f'с исполнителем <b>{str_user}</b>\n'
        f'и описанием <b>{str_description}</b>'
    )
    if new_task.status == 'In Progress':
        message_to_send += f'\nИ {str_user} уже приступил к задаче поставив статус <b>{new_task.status}</b>'
    if new_task.status == 'Done':
        message_to_send += f'\nИ {str_user} уже выполнил задачу поставив статус <b>{new_task.status}</b>'
    if tags is not None:
        message_to_send += f'\n{tags}'
    return message_to_send, provision


async def formatting_update_task(old_task, data):
    message_to_send = ''

    provision = False
    if old_task.id_projects == '655bed959f10a5e5a81baeb8':
        provision = True
    
    if old_task.title != data['title']:
        message_to_send += f'У задачи <b>{old_task.title}</b> изменился title на <b>{data["title"]}</b>\n'
    else:
        message_to_send += f'У задачи <b>"{old_task.title}"</b>\n'

    if old_task.description != data['description']:
        if old_task.description is None or old_task.description == '':
            old_description = 'не указано'
        else:
            old_description = old_task.description

        if data['description'] is None or data['description'] == '':
            new_description = 'не указано'
        else:
            new_description = data['description']
        message_to_send += f'изменилось описание с <b>{old_description}</b> на <b>{new_description}</b>\n'
    else:
        if old_task.description is None or old_task.description == '':
            old_description = 'не указано'
        else:
            old_description = '"' + old_task.description + '"'
        message_to_send += f'с описанием <b>{old_description}</b>\n'

    if old_task.id_users != data['id_users']:
        old_user = await get_users_in_db(old_task.id_users)
        if old_user is None:
            str_user_obj = 'не указан'
        else:
            str_user_obj = old_user.fio

        new_user = await get_users_in_db(data['id_users'])
        if new_user is None:
            str_new_user_obj = 'не указан'
        else:
            str_new_user_obj = new_user.fio
        message_to_send += f'изменился исполнитель с <b>{str_user_obj}</b> на <b>{str_new_user_obj}</b>\n'
    else:
        old_user = await get_users_in_db(old_task.id_users)
        if old_user is None:
            str_user_obj = 'не указан'
        else:
            str_user_obj = old_user.fio
        message_to_send += f'с исполнителем <b>"{str_user_obj}"</b>\n'

    if old_task.status != data['status']:
        message_to_send += f'изменился статус с <b>{old_task.status}</b> на <b>{data["status"]}</b>\n'
    else:
        message_to_send += f'со статусом <b>"{old_task.status}"</b>'
    return message_to_send, provision


async def formatting_old_free_sectors_list(old_free_sectors_list):
    message_to_send = 'Сектора исчезли\n'
    for sector in old_free_sectors_list:
        need_sectors_bool = [
            'Сектор A0' == sector,
            'Сектор A1' == sector,
            'Сектор A2' == sector,
            'Сектор A3' == sector,
            'Сектор A4' == sector,
            'Сектор C0' == sector,
            'Сектор C1' == sector,
            'Сектор C2' == sector,
            'Сектор C3' == sector,
            'Сектор C4' == sector,
        ]
        if any(need_sectors_bool):
            message_to_send += f'<b>{sector}</b>\n'
        else:
            message_to_send += f'{sector}\n'
    return message_to_send


async def formatting_new_free_sectors_list(new_free_sectors_list):
    message_to_send = 'Новые сектора\n'
    for sector in new_free_sectors_list:
        need_sectors_bool = [
            'Сектор A0' == sector,
            'Сектор A1' == sector,
            'Сектор A2' == sector,
            'Сектор A3' == sector,
            'Сектор A4' == sector,
            'Сектор C0' == sector,
            'Сектор C1' == sector,
            'Сектор C2' == sector,
            'Сектор C3' == sector,
            'Сектор C4' == sector,
        ]
        if any(need_sectors_bool):
            message_to_send += f'<b>{sector}</b>\n'
        else:
            message_to_send += f'{sector}\n'
    return message_to_send
