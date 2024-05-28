import os
from dotenv import load_dotenv

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TemplateSendMessage, TextSendMessage, TextMessage, PostbackEvent
from linebot.models import ButtonsTemplate, DatetimePickerTemplateAction
from testwise import google_calender

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

conversation_state = {'step': None, 'data': {},'topic': None, 'college': None}

def sendStartTime(event):
  try:
    message = TemplateSendMessage(
      alt_text='選取日期時間',
      template=ButtonsTemplate(
        thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
        title='面試開始時間',
        text='請選擇：',
        actions=[
          DatetimePickerTemplateAction(
            label="選取開始日期時間",
            data="action=start_time",
            mode="datetime",
            initial="2024-06-01T10:00",
            min="2024-01-01T00:00",
            max="2024-12-31T23:59"
          )
        ]
      )
    )
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

def sendEndTime(event):
  try:
    message = TemplateSendMessage(
      alt_text='選取結束日期時間',
      template=ButtonsTemplate(
        thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
        title='面試結束時間',
        text='請選擇：',
        actions=[
          DatetimePickerTemplateAction(
            label="選取結束日期時間",
            data="action=end_time",
            mode="datetime",
            initial="2024-06-01T12:00",
            min="2024-01-01T00:00",
            max="2024-12-31T23:59"
          )
        ]
      )
    )
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

def requestLocation(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text='請輸入面試地點')
  )

def requestDescription(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text='請輸入該場面試描述')
  )

def handleUserInput(event, conversation_state):
  step = conversation_state['step']

  if isinstance(event, PostbackEvent) and hasattr(event.postback, 'params'):
    if step == 'start_time':
      conversation_state['data']['start_time'] = event.postback.params['datetime']
      conversation_state['step'] = 'end_time'
      sendEndTime(event)
    elif step == 'end_time':
      conversation_state['data']['end_time'] = event.postback.params['datetime']
      conversation_state['step'] = 'location'
      requestLocation(event)
  elif isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
    if step == 'location':
      conversation_state['data']['location'] = event.message.text
      conversation_state['step'] = 'description'
      requestDescription(event)
    elif step == 'description':
      conversation_state['data']['description'] = event.message.text
      google_calender.CreateCalendarEvent(event, conversation_state['data'])
      conversation_state['step'] = None
      conversation_state['data'] = {}