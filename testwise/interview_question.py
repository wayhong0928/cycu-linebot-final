import os
from dotenv import load_dotenv

from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage
from testwise.models import InterviewQuestion

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

def sendInterviewQuestion(event, Department):
  try:
    unit = InterviewQuestion.objects.get(department_name = Department)
    message = [
      TextSendMessage(text="{}".format(unit.question_text)),
      TextSendMessage(text="{}".format(unit.answer_text)),
    ]
    line_bot_api.reply_message(event.reply_token, message)
  except InterviewQuestion.DoesNotExist:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "查無此資料！"))
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!{}'.format(e)))
