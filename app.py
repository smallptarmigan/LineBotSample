# -*- coding: utf-8 -*-

# Import package For reading line message function
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage)

# Import package For use google spreadsheet function
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Import package
import os
import json
import random
import datetime
from logging import getLogger, config

# Import myfile 
# Divide the file for each reply function
# To improve the readability of the program
import package.work
import package.spreadsheet as sp

app = Flask(__name__)

# Read setting file
# Read the TOKEN and ID in config file 
with open('data/lineconf.json', 'r') as f:
    CONF_DATA = json.load(f)

CHANNEL_ACCESS_TOKEN = CONF_DATA['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = CONF_DATA['CHANNEL_SECRET']

GROUP_MAIN_ID = CONF_DATA['GROUP_MAIN_ID']
GROUP_TEST_ID = CONF_DATA['GROUP_TEST_ID']

USER_ID = CONF_DATA['ADMIN_USERs']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Read google spreadsheet config file
# use creds to create a client to interact with the Google Drive API
wb = package.spreadsheet.authenticate_spreadsheet()
workschedule_sheet = wb.get_worksheet(0)
timesetting_sheet = wb.get_worksheet(1)
result_sheet = wb.get_worksheet(2)

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
        # Define debag code
        if get_text == "test":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="get test message!"))
        elif get_text == "reply":
            line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text='test push message!'))

        # Define help code
        package.help.explanation(get_text)
        # if out_text != None:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=out_text))

        # Tool
        if get_text in ["?????????"]:
            out_text = package.send_nextwork.make_send_text(package.send_nextwork.search_next_work(package.send_nextwork.read_work()))
        
        # set group
        if get_text in ["??????????????????"]:
            profile = line_bot_api.get_profile(event.source.user_id)

            wb = sp.authenticate_spreadsheet()
            timesetting_sheet = wb.get_worksheet(1)
            sheet_id = sp.search_id_sheet(timesetting_sheet, profile.user_id)

            if hasattr(event.source,"group_id"):
                timesetting_sheet.update_cell(3, sheet_id, event.source.group_id)
            if hasattr(event.source,"room_id"):
                timesetting_sheet.update_cell(3, sheet_id, event.source.room_id)

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="??????????????????????????????????????????"))

        # set time
        if "????????????" in get_text[:4]:
            profile = line_bot_api.get_profile(event.source.user_id)

            wb = sp.authenticate_spreadsheet()
            timesetting_sheet = wb.get_worksheet(1)
            sheet_id = sp.search_id_sheet(timesetting_sheet, profile.user_id)

            settime = get_text[4:]

            #debag
            #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=len(settime)))
            #limit_time = datetime.datetime.strptimEde(get_text[4:], '%H:%M')
            #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(limit_time)))      
            #limit_time = datetime.datetime.strptimEde(get_text, '%H:%M')

            timesetting_sheet.update_cell(6, sheet_id, settime)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="??????????????????????????????"))

        # run test
        if out_text == "runtest":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="????????????????????????"))

# Define sticher event (main funtion)
# 
#@handler.add(MessageEvent, message=StickerMessage)
#def handle_image(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text="Image"))

# Define sticker event
# 
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    dt_now = datetime.datetime.now()

    # spreadsheet setting
    wb = sp.authenticate_spreadsheet()
    workschedule_sheet = wb.get_worksheet(0)
    timesetting_sheet = wb.get_worksheet(1)
    result_sheet = wb.get_worksheet(2)

    profile = line_bot_api.get_profile(event.source.user_id)

    # user init
    if sp.search_id_sheet(timesetting_sheet, profile.user_id) == 0:
        timesetting_sheet.update_cell(1, len(timesetting_sheet.row_values(1))+1, profile.display_name)
        timesetting_sheet.update_cell(2, len(timesetting_sheet.row_values(2))+1, profile.user_id)
        timesetting_sheet.update_cell(23, len(timesetting_sheet.row_values(23))+1, 0)
        result_sheet.update_cell(1, len(result_sheet.row_values(1))+1, profile.display_name)
        workschedule_sheet.update_cell(1, len(workschedule_sheet.row_values(1))+1, profile.display_name)

    sheet_date = sp.search_date_sheet(result_sheet, dt_now)
    sheet_id = sp.search_id_sheet(timesetting_sheet, profile.user_id)

    # debag
    #output = str(sheet_date) + '-' + str(sheet_id)
    #test_profile = line_bot_api.get_profile(event.source)
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(profile.type)))

    # save time
    result_sheet.update_cell(sheet_date, sheet_id, dt_now.strftime('%H:%M'))

# Define main function
if __name__ == "__main__":
    # Set port default 8002(8001)
    port = int(os.getenv("PORT", 8002))

    # Flask is not exposed to the outside
    # Specify IP and port as arguments of run
    app.run(host="0.0.0.0", port=port)

    # [error] Send stop message (nonexecutable program)
    # Executed when line bot program does not start successfully for some reason or other.
    #line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text='[error] Line bot program could not start'))
