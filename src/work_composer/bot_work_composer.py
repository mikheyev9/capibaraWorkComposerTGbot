import datetime as dt

from requests import Session

from logging_to_project import logger_to_project


LOGIN = 'vi3sa@ya.ru'
PASSWORD = '09Area322'
EPOCH_MINSTAMP = 27924300
EPOCH_DT = dt.datetime(year=2023, month=2, day=4)
PACK_SIZE = 3


class WCSession(Session):
    def __init__(self):
        super().__init__()
        self._token = None
        self._organization = None
        self.user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        )

    def login(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '404',
            'origin': 'https://www.workcomposer.com',
            'pragma': 'no-cache',
            'referer': 'https://www.workcomposer.com/',
            'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent
        }
        data = {
            'username': LOGIN,
            'password': PASSWORD,
            'params': f'{{"username":"{LOGIN}","password":"{PASSWORD}"}}'
        }
        url = 'https://api2.workcomposer.com/security/login'
        response = self.post(url, data=data, headers=headers)
        if '"status":1' not in response.text:
            raise RuntimeError(f'WorkComposer login error! Login response:\n{response.text}')
        self._token = response.json()['auth']['token']
        self._organization = response.json()['auth']['_organization']

    def get_projects_from_work_composer(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '908',
            'origin': 'https://www.workcomposer.com',
            'pragma': 'no-cache',
            'referer': 'https://www.workcomposer.com/',
            'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent
        }
        response = self.post(
            'https://api.workcomposer.com/v1/project/',
            data={'authToken': self._token}, headers=headers
        )
        json_data = response.json()
        return json_data

    def get_task_from_work_composer(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '908',
            'origin': 'https://www.workcomposer.com',
            'pragma': 'no-cache',
            'referer': 'https://www.workcomposer.com/',
            'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent
        }
        response = self.post(
            'https://api2.workcomposer.com/task/',
            data={'authToken': self._token}, headers=headers
        )
        json_data = response.json()
        return json_data

    def get_users_from_work_composer(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '908',
            'origin': 'https://www.workcomposer.com',
            'pragma': 'no-cache',
            'referer': 'https://www.workcomposer.com/',
            'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent
        }
        response = self.post(
            'https://api2.workcomposer.com/organization/get-users',
            data={'authToken': self._token}, headers=headers
        )
        json_data = response.json()
        return json_data

    def create_task_in_work_composer(self, title: str, description: str, user, project):
        data = {
            'authToken': self._token,
            'title': title,
            'description': description,
            'priority': 2,
            '_assignee': None if user is None else user.id_in_work_composer,
            '_project': project.id_in_work_composer,
            '_sprint': None
        }
        url = 'https://api2.workcomposer.com/task/create'
        response = self.post(url, data=data)
        if response.status_code != 200:
            logger_to_project.error(f'Create task is not complite, response with {response.status_code}')

    def delete_task_in_work_composer(self, id_task: str):
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
            'authToken': self._token,
            '_id': id_task
        }
        url = 'https://api2.workcomposer.com/task/delete'
        response = self.post(url, data=data, headers=headers)
        if response.status_code != 200:
            logger_to_project.error(f'Delete task is not complite, response with {response.status_code}')


wcsession = WCSession()
wcsession.login()
