# -*- coding: utf-8 -*-

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

# Read schedule
def read_work():
    wb = sp.authenticate_spreadsheet()
    workschedule_sheet = wb.get_worksheet(0)
    timesetting_sheet = wb.get_worksheet(1)
    result_sheet = wb.get_worksheet(2)

    datelist = workschedule_sheet.col_values(1)
    workdata = workschedule_sheet.col_values(2)

    return [datelist, workdata]


def search_next_work(work_list):
    dt_now = datetime.datetime.now()
    now_date = dt_now.strftime("%Y/%m/%d")
    next_work_day = None

    dayafter = False
    [datelist, workdata] = work_list
    for i, w in enumerate(workdata):
        if dayafter:
            if w == '日勤':
                next_work_day = datelist[i]
                break
        if datelist[i] == now_date:
            dayafter = True

    return next_work_day

def add_tsuken_message(work_list, message=""):
    dt_now = datetime.datetime.now()
    now_date = dt_now.strftime("%Y/%m/%d")

    for i, d in enumerate(work_list):
        if d[0] == now_date:
            if d[5] == '提出':
                message += "\n通研提出可能日になりました。"
            elif d[5] == '締切':
                message += "\n通研提出締切が近くなりました。"
            elif d[5] == '採点':
                message += "\n通研の採点日です。"

    return message


def make_send_text(next_work_day, s=False):
    # print(next_work_day[0][9:])
    work_text = '次勤務は'+str(int(next_work_day[5:7]))+'月'+str(int(next_work_day[8:]))+'日'+'9:00 開始です'

    stamp_message = '6:15までにスタンプをお願いします'

    mezamashi = "1.毎日の次勤務確認\n2.目覚まし時計の3点確認\n3.起床後すぐの出勤時刻確認"

    print(work_text)
    if next_work_day == None:
        work_text = '次勤務が登録されていません。'
    if s:
        work_text += ('\n' + stamp_message)
        work_text += ('\n\n' + mezamashi)
    return work_text


if __name__ == "__main__":
    # Read schedule data
    work_list = read_work()
    next_work_day = search_next_work(work_list)
    message = make_send_text(next_work_day, s=True)
    #message = add_tsuken_message(work_list, message)
    print(message)
    line_bot_api.push_message(GROUP_MAIN_ID, TextSendMessage(text=message))
    #print(message)
