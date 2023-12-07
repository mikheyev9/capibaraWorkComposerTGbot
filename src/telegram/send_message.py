from crud.read_data_db import get_all_chat_id
from logging_to_project import logger_to_project
from settings.config import DEBUG, SKIP_CHAT_ID
from telegram.formatting_message_text import (formatting_new_free_sectors_list, formatting_new_task,
                                              formatting_old_free_sectors_list, formatting_update_task)


async def send_message_to_telegram(bot, message_text: str, provision: bool = False) -> None:
    all_chat_id = await get_all_chat_id()
    if DEBUG is False:
        for obj_chat_id in all_chat_id:
            chat_id = obj_chat_id[0].chat_id
            if chat_id in SKIP_CHAT_ID:
                continue
            try:
                await bot.send_message(chat_id, message_text, parse_mode='HTML')
            except Exception as error:
                logger_to_project.info(f'error with {chat_id = }, error is {error = }')
    else:
        chat_id = '-1001825841490'
        if provision:
            chat_id = '-1002091166610'
        try:
            await bot.send_message(chat_id, message_text, parse_mode='HTML')
        except Exception as error:
            logger_to_project.info(f'error with {chat_id = }, error is {error = }')


async def generate_message_to_send_from_module_parse_sectors(bot, message_to_send):
    await send_message_to_telegram(bot, message_to_send)


async def generate_message_to_send_from_google_sheets(bot, message_to_send):
    await send_message_to_telegram(bot, message_to_send)


async def generate_message_to_send_from_work_composer(bot, task_to_update: list, new_task_after_reset: list) -> None:
    if new_task_after_reset:
        for data_new_task in new_task_after_reset:
            new_task, tags = data_new_task
            message_to_send, provision = await formatting_new_task(new_task, tags)
            await send_message_to_telegram(bot, message_to_send, provision)

    if task_to_update:
        for update_data in task_to_update:
            old_task = update_data[0]
            data = update_data[1]
            message_to_send, provision = await formatting_update_task(old_task, data)
            await send_message_to_telegram(bot, message_to_send, provision)


async def generate_message_to_send_from_parse_sectors(
    bot,
    new_free_sectors_list: list,
    old_free_sectors_list: list
) -> None:
    if new_free_sectors_list:
        message_to_send = await formatting_new_free_sectors_list(new_free_sectors_list)
        await send_message_to_telegram(bot, message_to_send)

    if old_free_sectors_list:
        message_to_send = await formatting_old_free_sectors_list(old_free_sectors_list)
        await send_message_to_telegram(bot, message_to_send)
