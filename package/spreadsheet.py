# -*- coding: utf-8 -*-

from re import A
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import os
import json
import datetime

def authenticate_spreadsheet():
    # Read google spreadsheet config file
    # use creds to create a client to interact with the Google Drive API
    # 'data/_googleclient.json' -> 'data/googleclient.json' (Remove underbar)
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('data/_googleclient.json', scope)
    client = gspread.authorize(creds)
    # Make sure you use the right name here.
    # 'data/_spreadsheetkey.json' -> 'data/spreadsheetkey.json' (Remove underbar)
    with open('data/_spreadsheetkey.json', 'r') as f:
        CONF_DATA = json.load(f)
    wb = client.open_by_key(CONF_DATA['SPREADSHEET_KEY'])
    return wb

def search_name_sheet(sheet, name:str):
    name_row = -1
    sheet_row = sheet.row_values(1)
    for i, row in enumerate(sheet_row):
        if row == name:
            name_row = i
            break
    return name_row + 1

def search_date_sheet(sheet, dt_now):
    date_col = -1
    today = dt_now.strftime('%Y/%m/%d')
    sheet_col = sheet.col_values(1)
    for i, col in enumerate(sheet_col):
        if col == today:
            date_col = i
            break
    if date_col == -1:
        sheet.update_cell(len(sheet_col)+1, 1, today)
        date_col = len(sheet_col)
    return date_col + 1

def stamp_sheet(sheet, name:str):
    dt_now = datetime.datetime.now()
    row = search_name_sheet(sheet, name)
    col = search_date_sheet(sheet, dt_now)
    sheet.update_cell(col, row, dt_now.strftime('%H:%M'))

# Define main function
# Test code
if __name__ == "__main__":
    #ABS_PATH = os.path.dirname(os.path.abspath(__file__))

    # Read google spreadsheet config file
    # Find a workbook by name and open sheet
    wb = authenticate_spreadsheet()
    
    workschedule_sheet = wb.get_worksheet(0)
    timesetting_sheet = wb.get_worksheet(1)
    result_sheet = wb.get_worksheet(2)

    # Extract and print all of the values
    #dt_now = datetime.datetime.now()
    #result_sheet.update_cell(2, 2, dt_now.strftime('%H:%M'))
    #print(search_name_sheet(timesetting_sheet, "test"))
    #print(search_date_sheet(workschedule_sheet, dt_now))
    stamp_sheet(result_sheet, "test")
    
    


