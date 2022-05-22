# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage)
import os
import sys
import csv
import json
import datetime
from logging import getLogger, config
import difflib
import requests

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

config.fileConfig('data/_logging.conf')
logger = getLogger(__name__)

# Read schedule
def read_work():
    workdata = []
    with open('data/workday.csv', encoding = "utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            workdata.append([str(i) for i in row])
    # line_bot_api.push_message(USER_ID[0], TextSendMessage(text=workdata))
    # line_bot_api.push_message(USER_ID[0], TextSendMessage(text='read schedule'))
    return workdata


def search_next_work(work_list):
    dt_now = datetime.datetime.now()
    now_date = dt_now.strftime("%Y/%m/%d")
    next_work_day = None
    #print(now_date)

    dayafter = False
    for i, d in enumerate(work_list):
        if dayafter:
            if d[2] == '日勤':
                next_work_day = work_list[i]
                break
        #print(d[0], now_date)
        if d[0] == now_date:
            dayafter = True
        #print(d[0])
        #print(d[0] == "2021/08/10")
        #print(d[0] - now_date)
        #print(difflib.context_diff(d[0], now_date))

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
    stamp_message = '6時15分までにメッセージかスタンプをお願いします。'
    work_text = '次勤務は'+next_work_day[0][8:]+'日'+next_work_day[1]+'曜日'+next_work_day[3][0:1]+'時からです。'
    if next_work_day == None:
        work_text = '次勤務が登録されていません。'
    if s:
        work_text += ('\n' + stamp_message)
    return work_text


if __name__ == "__main__":
    # Send root
    #line_bot_api.push_message(USER_ID[0], TextSendMessage(text='send next work time!'))
    #line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text='次勤務は2日月曜日9時からです。\n6時15分までにメッセージかスタンプをお願いします。'))

    # Read schedule data
    work_list = read_work()
    next_work_day = search_next_work(work_list)
    message = make_send_text(next_work_day, s=True)
    message = add_tsuken_message(work_list, message)
    line_bot_api.push_message(GROUP_TEST_ID, TextSendMessage(text=message))
    #print(message)

    at_day = next_work_day[0][5:7] + next_work_day[0][8:] + next_work_day[0][0:4]
    print(at_day)

    # print(work_list)
    # print(message)