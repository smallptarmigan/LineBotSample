# -*- coding: utf-8 -*-

from re import A
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import os
import json
import datetime



def test_certification():
    pass

def search_name_sheet(sheet, name):
    name_row = -1
    for i in range(1, sheet.col_count):
        if sheet.cell(1, i).value == name:
            name_row = i
            break
    return name_row

# Define main function
# Test code
if __name__ == "__main__":
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))

    # Read google spreadsheet config file
    # use creds to create a client to interact with the Google Drive API
    # 'data/_googleclient.json' -> 'data/googleclient.json' (Remove underbar)
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('data/_googleclient.json', scope)
    client = gspread.authorize(creds)
      
    # Find a workbook by name and open sheet
    # Make sure you use the right name here.
    # 'data/_spreadsheetkey.json' -> 'data/spreadsheetkey.json' (Remove underbar)
    with open('data/_spreadsheetkey.json', 'r') as f:
        CONF_DATA = json.load(f)
    wb = client.open_by_key(CONF_DATA['SPREADSHEET_KEY'])
    workschedule_sheet = wb.get_worksheet(0)
    timesetting_sheet = wb.get_worksheet(1)
    result_sheet = wb.get_worksheet(2)

    # Extract and print all of the values
    #dt_now = datetime.datetime.now()
    #result_sheet.update_cell(2, 2, dt_now.strftime('%H:%M'))
    print(search_name_sheet(timesetting_sheet, "tester"))
    
    


