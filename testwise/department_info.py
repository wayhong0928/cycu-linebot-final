import os
from dotenv import load_dotenv

from linebot import LineBotApi, WebhookParser
from linebot.models import  TextSendMessage
from testwise.models import DepartmentInfo

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

def sendInterviewQuestion(event, Department):
  try:
    unit = DepartmentInfo.objects.get(department_name = Department)
    message = [
      TextSendMessage(text="科系名稱：{}".format(unit.department_name)),
      TextSendMessage(text="必修科目網址：\n{}".format(unit.compulsory_courses)),
      TextSendMessage(text="英文畢業門檻：\n{}".format(unit.graduation_requirements)),
    ]
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!{}'.format(e)))
