# -*- coding: utf-8 -*-

from __future__ import barry_as_FLUFL
from operator import truediv
from tokenize import group
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage)
import csv
import json
import datetime
from logging import getLogger, config

import package.spreadsheet as sp

app = Flask(__name__)

# Read data file
with open('data/_lineconf.json', 'r') as f:
    CONF_DATA = json.load(f)

CHANNEL_ACCESS_TOKEN = CONF_DATA['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = CONF_DATA['CHANNEL_SECRET']
GROUP_MAIN_ID = CONF_DATA['GROUP_MAIN_ID']
GROUP_TEST_ID = CONF_DATA['GROUP_TEST_ID']
USER_ID = CONF_DATA['ADMIN_USERs']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

if __name__ == "__main__":
    dt_now = datetime.datetime.now()

    # setting spreadsheet
    wb = sp.authenticate_spreadsheet()
    workschedule_sheet = wb.get_worksheet(0)
    timesetting_sheet = wb.get_worksheet(1)
    result_sheet = wb.get_worksheet(2)

    # data extraction
    user_names = timesetting_sheet.row_values(1)
    user_ids = timesetting_sheet.row_values(2)
    group_ids = timesetting_sheet.row_values(3)
    work_data = workschedule_sheet.row_values(sp.search_date_sheet(workschedule_sheet, dt_now))
    limit_data = timesetting_sheet.row_values(6)
    result_data = result_sheet.row_values(sp.search_date_sheet(result_sheet, dt_now))
    count_data = timesetting_sheet.row_values(23)

    # check time
    for i, id in enumerate(user_ids):
        # not user
        if i == 0:
            continue

        # Confirmation of working days
        if len(work_data) > i+1:
            user_work = work_data[i+1]
        else:
            user_work = work_data[1]

        if user_work == "日勤":
            # Confirmation of wake-up time registration
            if len(limit_data) < i+1:
                print("[error:101] no wake-up time registration " + user_names[i])
                continue
            elif limit_data[i] == "":
                print("[error:102] no wake-up time registration " + user_names[i])
                continue
            timelimit = limit_data[i]

            # Check the time
            # Overtime and nostamp
            worning_flag = False
            timelimit = datetime.datetime.strptime(timelimit, '%H:%M')
            timelimit = timelimit.replace(year=dt_now.year, month=dt_now.month, day=dt_now.day)
            #dt_now = dt_now + datetime.timedelta(hours=3)
            #print(timelimit, dt_now)
            if timelimit < dt_now:
                if len(result_data) < i+1:
                    worning_flag = True
                elif result_data[i] == "":
                    worning_flag = True
            else:
                #print("[error:103] off time " + user_names[i])
                continue

            # Warning message (for grope) 
            if worning_flag and count_data[i] < 3:
                count_data[i] = int(count_data[i]) + 1
                timesetting_sheet.update_cell(23, i+1, count_data[i])
                outputmessage1 = "!!!警告メッセージ!!!\n" + user_names[i] + "の起床が確認できません\n" + "早急に連絡してください"
                #print(outputmessage1)
                line_bot_api.push_message(group_ids[i], TextSendMessage(text=outputmessage1))
            else:
                timesetting_sheet.update_cell(23, i+1, 0)

            # Report to administrator
            if count_data[i] == 3:
                outputmessage2 = "!!!警告メッセージ!!!\n" + user_names[i] + "15分以上の遅延が発生しています\n" + "管理者への報告を行います"
                #print(outputmessage2)
                line_bot_api.push_message(group_ids[i], TextSendMessage(text=outputmessage2))

        # debag prog
        #print(i, user_names[i], user_work)
        # if i == 1:
        #     break

    