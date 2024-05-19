import os
import django
from dotenv import load_dotenv
from urllib.request import Request

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

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

    # 這裡放置建立行事曆事件的程式碼
    # 例如：
    event_data = {
        'summary': 'TEST',
        'location': 'CYCU_IM',
        'description': 'TEST',
        'start': {
            'dateTime': '2024-05-20T10:00:00',
            'timeZone': 'Asia/Taipei',
        },
        'end': {
            'dateTime': '2024-05-20T12:00:00',
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