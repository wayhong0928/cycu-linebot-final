import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage, ImagemapSendMessage, BaseSize, MessageImagemapAction, ImagemapArea

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

# 學院對應科系列表
college_departments = {
    "商學院": ["會計學系", "財務金融學系", "國際經營與貿易系", "資訊管理學系", "企業管理學系", "國際商學學士學程"],
    "設計學院": ["建築學系", "室內設計學系", "商業設計學系", "地景建築學系", "社會設計學士學位學程"],
    "電資學院": ["電子工程學系", "電機工程學系", "資訊工程學系", "工業與系統工程學系", "電機資訊學院學士班"],
    "理學院": ["化學系", "心理學系", "生物科技學系", "物理學系", "應用數學系", "理學院學士學位學程"],
    "工學院": ["化學工程學系", "機械工程學系", "土木工程學系", "環境工程學系", "生物醫學工程學系"],
    "法學院": ["財經法律學系", "應用華語文學系", "特殊教育學系", "應用外國語文學系", "人文與教育學院學士學程"],
    "人文與教育學院": ["財經法律學系", "應用華語文學系", "特殊教育學系", "應用外國語文學系", "人文與教育學院學士學程"]
}

# event, base_url = url, text = subjects
# this functions has 6 subjects.
def sendDepartmentTemplateSix(event, url, subjects):
  try:
    imgwidth = 1040
    imgheight = 1274
    message = [
      ImagemapSendMessage(
        base_url = url,
        alt_text="選擇科系",
        base_size=BaseSize(width = imgwidth, height = 1274), #圖片寬、高
        actions=[
          MessageImagemapAction( text = subjects[0], area = ImagemapArea( x = 0, y = imgheight * 0.25, width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[1], area = ImagemapArea( x = 0, y = imgheight * 0.5,  width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[2], area = ImagemapArea( x = 0, y = imgheight * 0.75, width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[3], area = ImagemapArea( x = imgwidth * 0.5, y= imgheight * 0.25, width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[4], area = ImagemapArea( x = imgwidth * 0.5, y= imgheight * 0.5,  width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[5], area = ImagemapArea( x = imgwidth * 0.5, y= imgheight * 0.75, width = imgwidth * 0.5, height = imgheight * 0.25))
        ]
      ),
      TextSendMessage(text="請點選科系，僅限一次：")
    ]
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!{}'.format(e)))
  
# event, base_url = url, text = subjects
# this functions has 5 subjects.
def sendDepartmentTemplateFive(event, url, subjects):
  try:
    imgwidth   = 1040
    imgheight = 1274
    message = [
      ImagemapSendMessage(
        base_url = url, 
        alt_text="選擇科系",
        base_size=BaseSize(width = imgwidth, height = 1274), #圖片寬、高
        actions=[
          MessageImagemapAction( text = subjects[0], area = ImagemapArea( x = 0, y = imgheight * 0.25, width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[1], area = ImagemapArea( x = 0, y = imgheight * 0.5,  width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[2], area = ImagemapArea( x = imgwidth * 0.5, y = imgheight * 0.25, width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[3], area = ImagemapArea( x = imgwidth * 0.5, y = imgheight * 0.5,  width = imgwidth * 0.5, height = imgheight * 0.25)),
          MessageImagemapAction( text = subjects[4], area = ImagemapArea( x = 0, y = imgheight * 0.75, width = imgwidth, height = imgheight * 0.25))
        ]
      ),
      TextSendMessage(text="請點選科系，僅限一次："),
    ]
    line_bot_api.reply_message(event.reply_token, message)
  except Exception as e:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!{}'.format(e)))
