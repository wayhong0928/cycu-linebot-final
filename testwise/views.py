import os
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, PostbackEvent, MessageAction, QuickReply, QuickReplyButton
from urllib.parse import parse_qsl
from testwise import life_function, dress_code, web_link, interview_question, department_info, department_template, user_input_calender

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

InterviewQuestion_name = False
DepartmentInfo_name = False
conversation_state = {'step': None, 'data': {},'topic': None, 'college': None}

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
          elif mtext == '生活機能':
            life_function.sendLifeFunction(event)
          elif mtext == '快速連結':
            web_link.sendWebLink(event)
          elif mtext == '建立面試行事曆':
            conversation_state['step'] = 'start_time'
            user_input_calender.sendStartTime(event)
          elif mtext == '面試建議' or mtext == '必修科目':
            conversation_state['topic'] = mtext
            sendQuickReply(event)
          elif conversation_state['topic'] in ['面試建議', '必修科目']:
            if conversation_state['college'] is None:
              conversation_state['college'] = mtext
              if mtext == "商學院":
                department_template.sendDepartmentTemplateSix(event, 'https://imgur.com/Z5URxrC.png', department_template.college_departments.get(mtext, []))
              elif mtext == "設計學院":
                department_template.sendDepartmentTemplateFive(event, 'https://imgur.com/Ohtoz4s.png', department_template.college_departments.get(mtext, []))
              elif mtext == "電資學院":
                department_template.sendDepartmentTemplateFive(event, 'https://imgur.com/EfcpLQY.png', department_template.college_departments.get(mtext, []))
              elif mtext == "理學院":
                department_template.sendDepartmentTemplateSix(event, 'https://imgur.com/G6GgTyH.png', department_template.college_departments.get(mtext, []))
              elif mtext == "工學院":
                department_template.sendDepartmentTemplateFive(event, 'https://imgur.com/lzm1CcD.png', department_template.college_departments.get(mtext, []))
              elif mtext in ["法學院", "人文與教育學院"]:
                department_template.sendDepartmentTemplateFive(event, 'https://imgur.com/DXkjeYZ.png', department_template.college_departments.get(mtext, []))
              else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇學院"))
            else:
              department = mtext
              topic = conversation_state['topic']
              conversation_state['topic'] = None
              conversation_state['college'] = None
              if topic == '面試建議':
                interview_question.sendInterviewQuestion(event, department)
              elif topic == '必修科目':
                department_info.sendInterviewQuestion(event, department)
          elif conversation_state['step']:
            user_input_calender.handleUserInput(event, conversation_state)
          else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mtext))


      elif isinstance(event, PostbackEvent):
        backData = dict(parse_qsl(event.postback.data))
        if backData.get('action') == 'room':
          life_function.sendBack_room(event)
        elif backData.get('action') == 'food':
          life_function.sendBack_food(event)
        elif backData.get('action') == 'traffic':
          life_function.sendBack_traffic(event)
        elif backData.get('action') == 'boy':
          dress_code.sendBack_boy(event)
        elif backData.get('action') == 'girl':
          dress_code.sendBack_girl(event)
        elif backData.get('action') == 'mix':
          dress_code.sendBack_mix(event)
        elif conversation_state['step']:
          user_input_calender.handleUserInput(event, conversation_state)

    return HttpResponse()
  else:
    return HttpResponseBadRequest()

def sendQuickReply(event):
  try:
    message = TextSendMessage(
      text='請選擇查詢學院',
      quick_reply=QuickReply(
        items=[
          QuickReplyButton( action = MessageAction( label = '商學院', text = '商學院')),
          QuickReplyButton( action = MessageAction( label = '設計學院', text = '設計學院')),
          QuickReplyButton( action = MessageAction( label = '電資學院', text = '電資學院')),
          QuickReplyButton( action = MessageAction( label = '理學院', text = '理學院')),
          QuickReplyButton( action = MessageAction( label = '工學院', text = '工學院')),
          QuickReplyButton( action = MessageAction( label = '法學院', text = '法學院')),
          QuickReplyButton( action = MessageAction( label = '人文與教育學院', text = '人文與教育學院'))
        ]
      )
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='傳送快速回覆發生錯誤！'))

def handleUserMessage(event, mtext):
  global InterviewQuestion_name
  global DepartmentInfo_name

  if InterviewQuestion_name:
    Department = mtext
    InterviewQuestion_name = False
    interview_question.sendInterviewQuestion(event, Department)
  elif DepartmentInfo_name:
    Department = mtext
    DepartmentInfo_name = False
    department_info.sendInterviewQuestion(event, Department)
  elif conversation_state['step']:
    user_input_calender.handleUserInput(event, conversation_state)
  else:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mtext))
