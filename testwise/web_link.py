import os
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage, TextMessage, PostbackEvent, PostbackTemplateAction, LocationSendMessage, CarouselColumn
from linebot.models import ButtonsTemplate, CarouselTemplate
from linebot.models import BubbleContainer, ImageComponent, BoxComponent, TextComponent
from linebot.models import IconComponent, ButtonComponent, SeparatorComponent, DatetimePickerAction, PostbackAction, URITemplateAction
from linebot.models import FlexSendMessage, URIAction, MessageAction
from urllib.parse import parse_qsl
from testwise import google_calender, life_function, dress_code

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

def sendWebLink(event):
  try:
    message = TemplateSendMessage(
      alt_text='學校快速連結',
      template = CarouselTemplate(
        columns=[
          CarouselColumn(
            thumbnail_image_url='https://654d-59-124-200-61.ngrok-free.app/static/school.png',
            title='中原大學',
            text='提供學校各式網站的快速連結',
            actions=[
              URITemplateAction(
                label='中原大學首頁',
                uri= 'https://www.cycu.edu.tw/'                        
              ),
              URITemplateAction(
                label='學群探索',
                uri= 'https://acadm.cycu.edu.tw/%e5%ad%b8%e7%be%a4%e6%8e%a2%e7%b4%a2/'
              ),
              URITemplateAction(
                label='學雜費收費標準表',
                uri= 'https://acct.cycu.edu.tw/category/%E5%AD%B8%E9%9B%9C%E8%B2%BB/%E5%AD%B8%E9%9B%9C%E8%B2%BB%E6%94%B6%E8%B2%BB%E6%A8%99%E6%BA%96/'
              )
            ]
          ),
          CarouselColumn(
            thumbnail_image_url='https://654d-59-124-200-61.ngrok-free.app/static/school.png',
            title='中原大學',
            text='提供學校各式網站的快速連結',
            actions=[
              URITemplateAction(
                label='I-TOUCH',
                uri= 'https://itouch.cycu.edu.tw/home/#/ann'                        
              ),
              URITemplateAction(
                label='開課查詢系統',
                uri= 'https://itouch.cycu.edu.tw/active_system/CourseQuerySystem/'
              ),
              URITemplateAction(
                label='學生宿舍資訊',
                uri= 'https://oosa.cycu.edu.tw/%e4%bd%8f%e5%ae%bf%e8%b3%87%e8%a8%8a/'
              )
            ]
          )
        ]                
      )
    )
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!{}'.format(e)))
