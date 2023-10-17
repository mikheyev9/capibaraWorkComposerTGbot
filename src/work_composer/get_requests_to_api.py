import requests
from settings.config import API_KEY_WORKCOMPOSER


async def __get_projects_from_work_composer():
    raise Exception('not used this function')
    response = requests.post(
        'https://api.workcomposer.com/v1/project/',
        data={'apiKey': API_KEY_WORKCOMPOSER}
    )
    json_data = response.json()
    return json_data


async def __get_task_from_work_composer():
    raise Exception('not used this function')
    response = requests.post(
        'https://api2.workcomposer.com/task/',
        data={'apiKey': API_KEY_WORKCOMPOSER}
    )
    json_data = response.json()
    return json_data


async def __get_users_from_work_composer():
    raise Exception('not used this function')
    response = requests.post(
        'https://api2.workcomposer.com/organization/get-users',
        data={'apiKey': API_KEY_WORKCOMPOSER}
    )
    json_data = response.json()
    return json_data
