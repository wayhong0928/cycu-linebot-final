import os
import django
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = None

def get_google_credentials():
    global creds
    """取得 Google 認證資訊"""
    credentials_path = "../token.json"
    if os.path.exists(credentials_path):
        creds = Credentials.from_authorized_user_file(credentials_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(credentials_path, "w") as token:
            token.write(creds.to_json())
    return creds

def CreateCalendarEvent(event):
  try:
    creds = get_google_credentials()
    service = build("calendar", "v3", credentials=creds)

    # 建立行事曆事件
    # ? 有辦法抓到面試的時間嗎？
    # TODO 要把學校、地點、面試描述跟時間當作參數帶進去

    event_data = {
        'summary': 'TEST',                     # 標題
        'location': 'CYCU_IM',                 # 地點，點擊可以跳google map 
        'description': 'TEST',                 # 描述
        'start': {                             # 開始時間與時區
            'dateTime': '2024-05-29T10:00:00',
            'timeZone': 'Asia/Taipei',
        },
        'end': {
            'dateTime': '2024-05-29T12:00:00',
            'timeZone': 'Asia/Taipei',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    event_data = service.events().insert(calendarId='primary', body=event_data).execute()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='活動已建立在 Google 日曆中！'))
  except HttpError as error:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤：{}'.format(error)))