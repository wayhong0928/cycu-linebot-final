import os
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import TemplateSendMessage, MessageTemplateAction, TextSendMessage
from linebot.models import ButtonsTemplate, PostbackTemplateAction

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
        text = '請選擇您的性別:',  #副標題
        actions=[
          PostbackTemplateAction(
            label='男性',
            data= 'action=boy',
            display_text='男性'
          ),
          PostbackTemplateAction(
            label='女性',
            data= 'action=girl',
            display_text='女性'
          ),
          PostbackTemplateAction(
            label='中性',
            data= 'action=mix',
            display_text='中性'
          )
        ]
      )
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))

def sendBack_boy(event):
  try:
    text1 = '❗男同學可以這樣穿❗\n'
    text1 += '下半身：卡其褲（深藍、卡其色）、乾淨的牛仔褲、西裝褲\n\n上半身：襯衫（素色、條紋、格子）、polo衫、合身不緊身的T恤\n\n鞋子：皮鞋（黑色、深咖啡色）、帆布鞋、乾淨的球鞋'  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))
    
def sendBack_girl(event):
  try:
    text1 = '❗女同學可以這樣穿❗\n'
    text1 += '下半身：長褲、裙子（不要短於膝上15公分）。避免熱褲\n\n上半身：以穿起來好看的上衣為主。避免太花、墜飾太多、過於暴露、無袖的上衣\n\n鞋子：皮鞋（黑色、深咖啡色）、帆布鞋、乾淨的球鞋、不要穿著會露出腳指頭的鞋子'  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))
    
def sendBack_mix(event):
  try:
    text1 = '❗同學可以這樣穿❗\n'
    text1 += '下半身：卡其褲（深藍、卡其色）、乾淨的牛仔褲、西裝褲、裙子。避免過於花俏的造型\n\n上半身：襯衫（素色、條紋、格子）、polo衫、合身不緊身的T恤。避免無袖的上衣\n\n鞋子：皮鞋（黑色、深咖啡色）、帆布鞋、乾淨的球鞋、不要穿著會露出腳指頭的鞋子'  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))