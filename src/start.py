import asyncio
import requests

#from google_sheets.main_google_sheets import main_google_sheets
from logging_to_project import logger_to_project
#from parse_sectors.if_change_event import main_if_change_event
from telegram.main_telegram import main_telegram


def main():
    ioloop = asyncio.get_event_loop()

    # ioloop.create_task(main_if_change_event())
    #ioloop.create_task(main_google_sheets())
    ioloop.create_task(main_telegram())

    ioloop.run_forever()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger_to_project.exception('Exception')
