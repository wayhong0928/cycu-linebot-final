import os
import datetime
from dotenv import load_dotenv
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage, TextMessage, PostbackEvent
from linebot.models import ButtonsTemplate
from linebot.models import BubbleContainer, ImageComponent, BoxComponent, TextComponent
from linebot.models import IconComponent, ButtonComponent, SeparatorComponent, DatetimePickerAction, PostbackAction
from linebot.models import FlexSendMessage, URIAction
from urllib.parse import parse_qsl

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

# Create your views here.


@csrf_exempt
def callback(request):
  # global input_friend_name
  if request.method == 'POST':
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
      events = parser.parse(body, signature)
    except InvalidSignatureError:
      return HttpResponseForbidden()
    except LineBotApiError:
      return HttpResponseBadRequest()
    
    for event in events:
      if isinstance(event, MessageEvent):
        if isinstance(event.message, TextMessage):
          line_bot_api.reply_message(event.reply_token, TextSendMessage(text = event.message.text))
        else:
          line_bot_api.reply_message(event.reply_token, TextSendMessage(text = event.message.text))
      
      if isinstance(event, PostbackEvent): # PostbackTemplateAction，觸發 Postback 事件
        backData = dict(parse_qsl(event.postback.data)) # 取得 Postback 資料
        if backData.get('action') == 'buy': 
          break
    return HttpResponse()
  else:
    return HttpResponseBadRequest()