from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

driver = webdriver.Chrome()
driver.get('https://www.anzen.mofa.go.jp/covid19/pdfhistory_world.html')

# ここでjsonfile名と2-2で用意したkeyを入力
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'gaimuscp2-9695fe220977.json', scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1P9MEQOwGI9hcnopg2Zdq4OOidJV1Rh87iTmtM00_vrs'
wb = gc.open_by_key(SPREADSHEET_KEY)

ws_info = wb.worksheet('info1')
ws_info.clear()
ws_list = wb.worksheet('赴任先リスト')

values_list1 = ws_list.col_values(1)
values_list2 = ws_list.col_values(2)

ws_info.update_cell(1, 1, '国名')
ws_info.update_cell(1, 2, '１. 日本からの渡航者や日本人に対して入国制限措置をとっている国・地域')

counter = 1

for value1, value2 in zip(values_list1, values_list2):

    counter += 1

    ws_info.update_cell(counter, 1, value1)

    if len(driver.find_elements_by_id(value2)) > 0:
        elem = driver.find_element_by_id(value2)
        if len(elem.text) > 45000:
            elem1 = elem.text[:int(len_text)]
            ws_info.update_cell(counter, 2, elem1)
            counter += 1
            elem2 = elem.text[int(len_text):]
            ws_info.update_cell(counter, 2, elem2)
        else:
            ws_info.update_cell(counter, 2, elem.text)


driver.quit()
