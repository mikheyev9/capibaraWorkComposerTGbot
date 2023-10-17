import requests
from logging_to_project import logger_to_project
from settings.config import API_KEY_WORKCOMPOSER


async def __delete_task_in_work_composer(id_task: str):
    raise Exception('not used this function')
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '460',
        'origin': 'https://www.workcomposer.com',
        'pragma': 'no-cache',
        'referer': 'https://www.workcomposer.com/',
        'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }
    data = {
        'apiKey': API_KEY_WORKCOMPOSER,
        '_id': id_task
    }
    url = 'https://api2.workcomposer.com/task/delete'
    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 200:
        logger_to_project.error(f'Delete task is not complite, response with {response.status_code}')
