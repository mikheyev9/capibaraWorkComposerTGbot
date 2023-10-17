from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from settings.config import (DATA_ABOUT_SERVICE_GOOGLE_ACCOUNT, EMAIL_USER,
                             SPREAD_SHEET_ID)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]


def auth_to_google_sheets():
    credentials = Credentials.from_service_account_info(
        info=DATA_ABOUT_SERVICE_GOOGLE_ACCOUNT,
        scopes=SCOPES
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    set_user_permissions_to_google_sheets(credentials)
    return service


def set_user_permissions_to_google_sheets(credentials):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': EMAIL_USER
    }

    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    drive_service.permissions().create(
        fileId=SPREAD_SHEET_ID,
        body=permissions_body,
        fields='id'
    ).execute()


service_google_sheets = auth_to_google_sheets()
