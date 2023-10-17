import requests
from logging_to_project import logger_to_project
from settings.config import API_KEY_WORKCOMPOSER


async def __create_task_in_work_composer(title: str, description: str, user, project):
    raise Exception('not used this function')
    if user is None:
        assignee = None
    else:
        assignee = user.id_in_work_composer
    data = {
        'apiKey': API_KEY_WORKCOMPOSER,
        'title': title,
        'description': description,
        'priority': 2,
        '_assignee': assignee,
        '_project': project.id_in_work_composer,
        '_sprint': None
    }
    url = 'https://api2.workcomposer.com/task/create'
    response = requests.post(url, data=data)
    if response.status_code != 200:
        logger_to_project.error(f'Create task is not complite, response with {response.status_code}')
