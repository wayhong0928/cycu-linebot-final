import os
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage, TextMessage, PostbackEvent, PostbackTemplateAction, LocationSendMessage
from linebot.models import ButtonsTemplate
from linebot.models import BubbleContainer, ImageComponent, BoxComponent, TextComponent
from linebot.models import IconComponent, ButtonComponent, SeparatorComponent, DatetimePickerAction, PostbackAction
from linebot.models import FlexSendMessage, URIAction, MessageAction
from urllib.parse import parse_qsl
from testwise import google_calender, life_function, dress_code, web_link, interview_question, department_info, department_template

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

InterviewQuestion_name = False
DepartmentInfo_name = False

# Create your views here.

@csrf_exempt
def callback(request):
  global InterviewQuestion_name
  global DepartmentInfo_name
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
          mtext = event.message.text
          if mtext == '服裝規定':
            dress_code.sendDressCode(event)
          elif mtext == '建立活動':
            google_calender.CreateCalendarEvent(event)
          elif mtext == '生活機能':
            life_function.sendLifeFunction(event)
          elif mtext == '快速連結':
            web_link.sendWebLink(event)
          elif mtext == '面試建議':
            department_template.sendDepartmentTemplate(event)
            InterviewQuestion_name = True
          elif mtext == '必修科目':
            department_template.sendDepartmentTemplate(event)
            DepartmentInfo_name = True
          else:
            if InterviewQuestion_name == True:
              Department = event.message.text
              interview_question.sendInterviewQuestion(event, Department)
            elif DepartmentInfo_name == True:
              Department = event.message.text
              department_info.sendInterviewQuestion(event, Department)
            else:
              line_bot_api.reply_message(event.reply_token, TextSendMessage(text = mtext))
        else:
          line_bot_api.reply_message(event.reply_token, TextSendMessage(text = mtext))

      if isinstance(event, PostbackEvent): # PostbackTemplateAction，觸發 Postback 事件
        backData = dict(parse_qsl(event.postback.data)) # 取得 Postback 資料
        if backData.get('action') == 'room':
          life_function.sendBack_room(event)
        elif backData.get('action') == 'food':
          life_function.sendBack_food(event)
        elif backData.get('action') == 'traffic':
          life_function.sendBack_traffic(event)
    return HttpResponse()
  else:
    return HttpResponseBadRequest()