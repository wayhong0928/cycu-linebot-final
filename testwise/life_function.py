import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage, TextMessage, PostbackEvent, PostbackTemplateAction, LocationSendMessage
from linebot.models import ButtonsTemplate
from linebot.models import BubbleContainer, ImageComponent, BoxComponent, TextComponent
from linebot.models import IconComponent, ButtonComponent, SeparatorComponent, PostbackAction
from linebot.models import FlexSendMessage, URIAction

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

def sendLifeFunction(event):
  try:
    bubble = BubbleContainer(
      direction = 'ltr', #項目左至右
      header = BoxComponent(
        layout = 'vertical', #垂直
        contents = [
          TextComponent(text='生活機能', weight='bold', size='xl'),
        ]
      ),
      hero = ImageComponent(
        url = 'https://imgur.com/9dri9pX.png',
        size = 'full',
        aspect_ratio = '792:650', #長寬比例
        aspect_mode = 'cover',
      ),
      body = BoxComponent(
        layout = 'vertical',
        contents = [
          TextComponent(text='機能', size='md'),
          BoxComponent(
            layout = 'baseline',
            margin = 'md',
            contents = [
              IconComponent(size='lg', url='https://imgur.com/H9wLmQd.png'),
              TextComponent(text='食', size='sm', color='#999999', flex=0),
              IconComponent(size='lg', url='https://imgur.com/3MzOu7o.png'),
              TextComponent(text='住', size='sm', color='#999999', flex=0),
              IconComponent(size='lg', url='https://imgur.com/iUWIO3W.png'),
              TextComponent(text='行', size='sm', color='#999999', flex=0),
            ]
          ),
          BoxComponent(
            layout = 'vertical',
            margin = 'lg',
            contents = [
              BoxComponent(
                layout = 'baseline',
                contents=[
                  TextComponent(text='學校地址', size='sm', color='#aaaaaa', flex=2),
                  TextComponent(text='320桃園市中壢區中北路200號', size='sm', color='#666666', flex=5),
                ],
              ),
              SeparatorComponent(color='#0000EF'), 
              BoxComponent(
                layout = 'baseline',
                contents=[
                  TextComponent(text='營業時間', size='sm', color='#aaaaaa', flex=2),
                  TextComponent(text='10:00 - 22:00', size='sm', color='#666666', flex=5),
                ],
              ),             
            ]
          ),
          BoxComponent(
            layout = 'horizontal',
            margin = 'xxl',
            spacing='md',
            contents = [
              ButtonComponent(
                style='primary',
                height='sm',
                action=PostbackAction(label='住宿',data= 'action=room',display_text='住宿'),
              ),
              ButtonComponent(
                style='secondary',
                height='sm',
                action=PostbackAction(label='飲食',data= 'action=food',display_text='飲食'),
              )
            ]
          ),
          BoxComponent(
            layout = 'horizontal',
            margin = 'xxl',
            spacing='md',
            contents = [
              ButtonComponent(
                style='primary',
                height='sm',
                action=PostbackAction(label='交通',data= 'action=traffic',display_text='交通'),
              ),
              ButtonComponent(
                style='secondary',
                height='sm',
                action=URIAction(label='電話', uri='tel:032659999'),
              )
            ]
          )
        ],
      ),
      footer = BoxComponent(
        layout = 'vertical',
        contents=[
          TextComponent(text='Copyright@testwise 2024', size='sm', color='#888888', align = 'center'),
        ]
      ),
    )
    message = FlexSendMessage(alt_text="生活機能", contents=bubble)
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))

def sendBack_room(event):
  try:
    text1 = '1.宿舍價位\n恩慈：每學期9000元\n良善：每學期12500元\n力行：每學期9500元'
    text1 += '\n2.租屋價位\n雅房：3000-5000\n五坪：5000-6000\n七~九坪：6500-8000\n個人小公寓：9000-12000\n家庭式：20000-25000'  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))
    
def sendBack_food(event):
  try:
    text1 = '中原夜市'  
    message = [
      TextSendMessage(
        text = text1
      ),
      LocationSendMessage(
        title = '中原夜市',
        address = '320桃園市中壢區實踐路日新路',
        latitude = 24.955863283190382, #緯度
        longitude = 121.24061399451166 #經度
      ), 
    ] 
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))

def sendBack_traffic(event):
  try:
    text1 = '公車155、156可達校內' 
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token, message)
  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '發生錯誤!'))