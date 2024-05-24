import os
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage, TextMessage, PostbackEvent, PostbackTemplateAction, LocationSendMessage, ImagemapSendMessage
from linebot.models import ButtonsTemplate, BaseSize
from linebot.models import BubbleContainer, ImageComponent, BoxComponent, TextComponent
from linebot.models import IconComponent, ButtonComponent, SeparatorComponent, DatetimePickerAction, PostbackAction
from linebot.models import FlexSendMessage, URIAction, MessageAction, MessageImagemapAction, ImagemapArea
from urllib.parse import parse_qsl


load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

def sendDepartmentTemplate(event):
  try:
    image_url = 'https://imgur.com/czLUJcC.png'#商
    imgwidth = 242
    imgheight = 296
    message = [
      TextSendMessage(text="請點選科系："),
      ImagemapSendMessage(
        base_url = image_url,
        alt_text="選擇科系",
        base_size=BaseSize(height = imgheight, width = imgwidth), #圖片寬、高
        actions=[
          MessageImagemapAction( #顯示文字訊息
            text='會計學系',
            area=ImagemapArea( #設定圖片範圍
              x=0,
              y=0,
              width=imgwidth,
              height=imgheight*0.25
            )
          ),
          MessageImagemapAction( #顯示文字訊息
            text='財務金融學系',
            area=ImagemapArea( #設定圖片範圍
              x=0,
              y=0,
              width=imgwidth,
              height=imgheight*0.5
            )
          ),
          MessageImagemapAction( #顯示文字訊息
            text='國際經營與貿易學系',
            area=ImagemapArea( #設定圖片範圍
              x=0,
              y=0,
              width=imgwidth,
              height=imgheight*0.75
            )
          ),
          MessageImagemapAction( #顯示文字訊息
            text='資訊管理學系',
            area=ImagemapArea( #設定圖片範圍 #右邊出不來RRRRR
              x=0.5*imgwidth,
              y=imgheight*0.25,
              width=imgwidth,
              height=imgheight*0.25
            )
          ),
          MessageImagemapAction( #顯示文字訊息
            text='企業管理學系',
            area=ImagemapArea( #設定圖片範圍
              x=0,
              y=0,
              width=imgwidth*0.5,
              height=imgheight*0.5
            )
          ),
          MessageImagemapAction( #顯示文字訊息
            text='國際商學學士學程',
            area=ImagemapArea( #設定圖片範圍
              x=0,
              y=0,
              width=imgwidth*0.5,
              height=imgheight*0.75
            )
          ),
        ]
      )    
    ]
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!{}'.format(e)))
