import os
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage
from linebot.models import ButtonsTemplate

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

def sendDressCode(event):
  try:
    message = TemplateSendMessage(
      alt_text='服裝規定',
      template = ButtonsTemplate(
        thumbnail_image_url='https://hips.hearstapps.com/hmg-prod/images/1-1672047213.png?crop=0.499xw:1.00xh;0.501xw,0&resize=640:*',
        title = '服裝規定', #主標題
        text = '請選擇以下按鈕:',  #副標題
        actions=[
          MessageTemplateAction(
            label='男性',
            text= '❗男同學可以這樣穿❗\n下半身：卡其褲（深藍、卡其色）、乾淨的牛仔褲、西裝褲\n\n上半身：襯衫（素色、條紋、格子）、polo衫、合身不緊身的T恤\n\n鞋子：皮鞋（黑色、深咖啡色）、帆布鞋、乾淨的球鞋'
          ),
          MessageTemplateAction(
            label='女性',
            text= '❗女同學可以這樣穿❗\n下半身：長褲、裙子（不要短於膝上15公分）。避免熱褲\n\n上半身：以穿起來好看的上衣為主。避免太花、墜飾太多、過於暴露、無袖的上衣\n\n鞋子：皮鞋（黑色、深咖啡色）、帆布鞋、乾淨的球鞋、不要穿著會露出腳指頭的鞋子'
          ),
          MessageTemplateAction(
            label='中性',
            text= '❗同學可以這樣穿❗\n下半身：卡其褲（深藍、卡其色）、乾淨的牛仔褲、西裝褲、裙子。避免過於花俏的造型\n\n上半身：襯衫（素色、條紋、格子）、polo衫、合身不緊身的T恤。避免無袖的上衣\n\n鞋子：皮鞋（黑色、深咖啡色）、帆布鞋、乾淨的球鞋、不要穿著會露出腳指頭的鞋子'
          )
        ]
      )
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))
