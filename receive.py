# -*- coding: utf-8 -*-

# Import package For reading line message function
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage)

# Import package
import os
import json
import random
import datetime
from logging import getLogger, config

# Import myfile 
# Divide the file for each reply function
# To improve the readability of the program
import package.testcode

app = Flask(__name__)

# Read setting file
# Save the TOKEN and ID in config file 
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(ABS_PATH+'/conf.json', 'r') as f:
    CONF_DATA = json.load(f)

CHANNEL_ACCESS_TOKEN = CONF_DATA['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = CONF_DATA['CHANNEL_SECRET']

GROUP_MAIN_ID = CONF_DATA['GROUP_MAIN_ID']
GROUP_TEST_ID = CONF_DATA['GROUP_TEST_ID']

USER_ID = CONF_DATA['ADMIN_USERs']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Setting log file
config.fileConfig('logging.conf')
logger = getLogger(__name__)

# Test GET and POST method
# This function can check the status of the network 
@app.route("/test", methods=['GET', 'POST'])
def test():
    return 'I\'m alive!'

# Define callback
# Handler definition
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Define message event (main funtion)
# 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_text = event.message.text
    randnum  = random.randint(0, 100)

    if True:
        # debag
        if get_text == "test":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="get test message!"))
        elif get_text == "reply":
            line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text='test push message!'))

        # test
        if get_text == "testimage":
            # image27 = linebot.models.ImageSendMessage(original_content_url="https://dsmpt.info/image/27.jpg")
            # line_bot_api.reply_message(event.reply_token, image27)
            pass
        if get_text == "testcode":
            test_text = package.testcode.test(get_text)
            line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text=test_text))

        # help
        out_text = help.explanation(get_text)
        if out_text != None:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=out_text))

        # Tool
        out_text = None
        if get_text in ["時間", "117", "時刻", "time"]:
            dt_now = datetime.datetime.now()
            out_text = dt_now.strftime('%m月%d日%H:%M:%Sです')
        if get_text in ["天気", "177", "weather", "今日の天気", "明日の天気"]:
            out_text = package.weather.get_weatherreport()
        if get_text in ["次勤務"]:
            out_text = package.send_nextwork.make_send_text(package.send_nextwork.search_next_work(package.send_nextwork.read_work()))
        # reply
        if out_text != None:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=out_text))

        # train time
        out_text = package.train.traintime(get_text)
        # reply
        if out_text != None:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=out_text))

# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text="Image"))

# sticker event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    if True:
        dt_now = datetime.datetime.now()
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=dt_now.strftime('%Y %m %d %H:%M:%S')))

if __name__ == "__main__":
    # Set port 8002(8001)
    port = int(os.getenv("PORT", 8002))
    # Flaskはデフォルトだと実行しても外部公開されないので、runの引数にIPとポートを指定する
    app.run(host="0.0.0.0", port=port)


    # [error] Send stop message (nonexecutable program)
    # Executed when line bot program does not start successfully for some reason or other.
    line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text='[error] Line bot program could not start'))
