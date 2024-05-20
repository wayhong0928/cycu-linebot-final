import os
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TemplateSendMessage, MessageTemplateAction, TextSendMessage, TextMessage, PostbackEvent, PostbackTemplateAction
from linebot.models import ButtonsTemplate
from linebot.models import BubbleContainer, ImageComponent, BoxComponent, TextComponent
from linebot.models import IconComponent, ButtonComponent, SeparatorComponent, DatetimePickerAction, PostbackAction
from linebot.models import FlexSendMessage, URIAction, MessageAction
from urllib.parse import parse_qsl
from testwise import google_calender

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
          mtext = event.message.text
          if mtext == '服裝規定':
            sendButton(event)
          elif mtext == '建立活動':
            google_calender.CreateCalendarEvent(event)
          elif mtext == '生活機能':
            sendFlex(event)
          else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = mtext))
        else:
          line_bot_api.reply_message(event.reply_token, TextSendMessage(text = mtext))

      '''if isinstance(event, PostbackEvent): # PostbackTemplateAction，觸發 Postback 事件
        backData = dict(parse_qsl(event.postback.data)) # 取得 Postback 資料
        if backData.get('action') == 'buy':
          break'''
    return HttpResponse()
  else:
    return HttpResponseBadRequest()

def sendButton(event):
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

def sendFlex(event):
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
                action=MessageAction(label='住宿', text='1.恩慈/良善/力行宿舍\n2.租屋價位\n雅房：3000-5000\n五坪：5000-6000\n七~九坪：6500-8000\n個人小公寓：9000-12000\n家庭式：20000-25000'),
              ),
              ButtonComponent(
                style='secondary',
                height='sm',
                action=MessageAction(label='飲食', text='中原夜市'),
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
                action=MessageAction(label='交通', text='公車155、156可達校內'),
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
