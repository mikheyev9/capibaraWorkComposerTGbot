import os
from pathlib import Path

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot


BASE_DIR = Path(__file__).parent.parent.parent
DOTENV_PATH = Path.joinpath(BASE_DIR, '.env')
load_dotenv(DOTENV_PATH)


DEBUG = True

if DEBUG is False:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    #BOT_TOKEN_ALERT_SECTORS_AND_EVENTS = os.getenv('BOT_TOKEN_ALERT_SECTORS_AND_EVENTS')
else:
    BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
    #BOT_TOKEN_ALERT_SECTORS_AND_EVENTS = os.getenv('TEST_BOT_TOKEN')

bot = AsyncTeleBot(BOT_TOKEN)
#bot_alert_sectors_and_events = AsyncTeleBot(BOT_TOKEN_ALERT_SECTORS_AND_EVENTS)

SKIP_CHAT_ID = ['346819032', '472533395']
API_KEY_WORKCOMPOSER = os.getenv('API_KEY_WORKCOMPOSER')

DATABASE_URL = os.getenv('DATABASE_URL').replace('./', '../')

# EMAIL_USER = os.environ['EMAIL']
# DATA_ABOUT_SERVICE_GOOGLE_ACCOUNT = {
#     'type': os.environ['TYPE'],
#     'project_id': os.environ['PROJECT_ID'],
#     'private_key_id': os.environ['PRIVATE_KEY_ID'],
#     'private_key': os.environ['PRIVATE_KEY'],
#     'client_email': os.environ['CLIENT_EMAIL'],
#     'client_id': os.environ['CLIENT_ID'],
#     'auth_uri': os.environ['AUTH_URI'],
#     'token_uri': os.environ['TOKEN_URI'],
#     'auth_provider_x509_cert_url': os.environ['AUTH_PROVIDER_X509_CERT_URL'],
#     'client_x509_cert_url': os.environ['CLIENT_X509_CERT_URL']
# }
# SPREAD_SHEET_ID = '18mM44Tg-gRZyI9DRSqpVXyOOftvX-jb5t-ctTYahkcE'
# WHITE_COLOR = {
#     'red': '1',
#     'blue': '1',
#     'green': '1'
# }
# GRAY_COLOR = {
#     'red': '0.8',
#     'blue': '0.8',
#     'green': '0.8'
# }
# GREEN_COLOR = {
#     'red': '0.20392157',
#     'blue': '0.3254902',
#     'green': '0.65882355'
# }
# ORANGE_COLOR = {
#     'red': '1',
#     'blue': '0',
#     'green': '1'
# }
