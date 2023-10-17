import asyncio

from crud.create_data_db import create_chat_id
from logging_to_project import logger_to_project
from parse_sectors.get_free_sectors import get_free_sectors
from settings.config import bot
from telegram.send_message import (generate_message_to_send_from_parse_sectors,
                                   generate_message_to_send_from_work_composer, send_message_to_telegram)
from work_composer.main_work_composer import create_and_update_task_from_work_composer, reset_data_in_db


@bot.message_handler(commands=['reset_data'])
async def reset(message):
    _ = await(create_chat_id({'chat_id': message.chat.id}))
    await reset_data_in_db()
    await bot.reply_to(message, "Все данные обновленны")


@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    _ = await create_chat_id({'chat_id': message.chat.id})
    if message.text == '/start' or message.text == '/reset_data':
        await bot.reply_to(message, message.text)
    else:
        if message.from_user.username is None:
            message_to_send = f'{message.from_user.first_name}: <b>{message.text}</b>'
        else:
            message_to_send = f'{message.from_user.username}: <b>{message.text}</b>'
        await send_message_to_telegram(bot, message_to_send)


async def send_message_if_change_status_or_add_new_task():
    import time
    while True:
        start_time = time.time()
        try:
            data = await create_and_update_task_from_work_composer()
            task_to_update, new_task_after_reset = data
            if task_to_update or new_task_after_reset:
                await generate_message_to_send_from_work_composer(bot, task_to_update, new_task_after_reset)
        except Exception:
            logger_to_project.exception('Exception')
        logger_to_project.info(f'telegram was worked {time.time() - start_time} sec')

        await asyncio.sleep(300)


async def alert_new_sectors():
    while True:
        new_free_sectors_list, old_free_sectors_list = get_free_sectors()
        await generate_message_to_send_from_parse_sectors(bot, new_free_sectors_list, old_free_sectors_list)
        await asyncio.sleep(30)


def main_telegram():
    ioloop = asyncio.get_event_loop()

    ioloop.create_task(bot.polling())
    ioloop.create_task(send_message_if_change_status_or_add_new_task())

    ioloop.run_forever()
