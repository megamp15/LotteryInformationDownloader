from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import os
import pandas as pd
import time

# TODO: FIX TIME DELAYS FOR THE FUNCTION BELOW. TRY USING ASYNC OR AWAIT FUNC IN PYTHON
driver = None


def auto_download(user_name, password, folder, retailer_num, close_window):
    global driver
    date_start = "04/01/2020"
    date_end = "05/02/2020"

    chromeOptions = Options()
    chromeOptions.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\Lottery\\"
            + folder
        },
    )
    chromeOptions.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        options=chromeOptions,
        executable_path="C:\\Users\\Mahir\\Desktop\\CS_PROJECTS\\AUTOLOGIN_DAD\\webDrivers\\chromedriver.exe",
    )

    driver.get("https://tx-lsp.lotteryservices.com/lsptx/public/lotteryhome")
    time.sleep(30)
    username_textbox = driver.find_element_by_id("username")
    first_login_button = driver.find_elements_by_class_name("btn")

    username_textbox.send_keys(user_name)
    first_login_button[0].submit()
    time.sleep(30)

    password_textbox = driver.find_element_by_id("password")
    second_login_button = driver.find_elements_by_class_name("btn")

    password_textbox.send_keys(password)
    second_login_button[0].submit()
    time.sleep(30)

    driver.get("https://tx-lsp.lotteryservices.com/lsptx/auth/viewreports")
    time.sleep(30)
    retailer = Select(driver.find_element_by_id("retailerId"))
    retailer.select_by_value(retailer_num)

    start_date = driver.find_element_by_id("startInvoiceDate")
    end_date = driver.find_element_by_id("endInvoiceDate")

    start_date.send_keys(date_start)
    end_date.send_keys(date_end)

    report_category = Select(driver.find_element_by_id("subCategoryCd"))
    report_category.select_by_value("-1")
    time.sleep(30)

    # Pack Inventory
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("2")
    time.sleep(30)

    date = driver.find_elements_by_xpath("//*[@id='rptTable']/tbody/tr/td[2]")
    csv = driver.find_elements_by_class_name("downloadcsv")

    count = 0
    for i in date:
        if i.text[:2] == date_start[:2]:
            csv[count].click()
            time.sleep(10)
            break
        count += 1

    time.sleep(30)
    # Pack Activated
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("4")
    time.sleep(30)

    csv = driver.find_elements_by_class_name("downloadcsv")

    for i in range(len(csv) - 1, -1, -1):
        csv[i].click()
        time.sleep(10)

    time.sleep(30)
    # Statement Summary
    report_name = Select(driver.find_element_by_id("reportName"))
    report_name.select_by_value("17")
    time.sleep(30)

    date = driver.find_elements_by_xpath("//*[@id='rptTable']/tbody/tr/td[2]")
    csv = driver.find_elements_by_class_name("downloadcsv")

    idx = []
    count = 0
    for i in date:
        if i.text[:2] == date_start[:2]:
            idx.append(count)
        count += 1
    idx.reverse()
    for i in idx:
        csv[i].click()
        time.sleep(10)

    if close_window == True:
        time.sleep(20)
        driver.close()


cur = os.getcwd()
Lottery_dir = cur + "\\" + "Lottery"
filelist = os.listdir(Lottery_dir)

# Delete all files in all folders in lottery
for x in filelist:
    del_file_dir = Lottery_dir + "\\" + x
    del_file_list = os.listdir(del_file_dir)
    print(del_file_list)
    for f in del_file_list:
        print(f)
        os.remove(del_file_dir + "\\" + f)


df = pd.read_excel(cur + "\\hidden.xlsx")
# print(df)
df.sort_values(by=["USERNAME"], inplace=True)
df = df.reset_index()
# print(df)

# for i in df["COMPANY"]:
#     if i in filelist:
#         print(i.strip())


# i = 0
# while i <= 21:
#     print(i)
#     user_name = df["USERNAME"][i].strip()
#     password = df["PASSWORD"][i].strip()
#     retailer_num = str(df["RETAILER NUMBER"][i]).strip()
#     folder = df["COMPANY"][i].strip()
#     try:
#         auto_download(user_name, password, folder, retailer_num, True)
#         # (df["RETAILER NUMBER"][i]).strip()
#     except:
#         print(df["COMPANY"][i])
#         try:
#             time.sleep(10)
#             driver.close()
#         except:
#             pass
#         pass
#     i += 1
# while df["USERNAME"][i] == df["USERNAME"][i + 1]:
#     i += 1
#     print(i, user_name, password, folder, retailer_num)
#     # auto_download(user_name, password, folder, retailer_num, False)
#     retailer_num = df["RETAILER NUMBER"][i]
#     folder = df["COMPANY"][i].strip()
# else:
#     print(i, user_name, password, folder, retailer_num)
#     # auto_download(user_name, password, folder, retailer_num, True)
# i += 1


# i = 0
# while i <= 22:
#     user_name = df["USERNAME"][i].strip()
#     password = df["PASSWORD"][i].strip()
#     retailer_num = df["RETAILER NUMBER"][i]
#     folder = df["COMPANY"][i].strip()
#     while df["USERNAME"][i] == df["USERNAME"][i + 1]:
#         i += 1
#         auto_download(user_name, password, folder, retailer_num, False)
#         retailer_num = df["RETAILER NUMBER"][i]
#         folder = df["COMPANY"][i].strip()
#         print("IN LOOP")
#     else:
#         auto_download(user_name, password, folder, retailer_num, False)
#         print("OUT LOOP")
#         for j in range(22, 30):
#             print("i: ", j)
#             try:
#                 auto_download(
#                     user_name, password, folder, df["RETAILER NUMBER"][i], False
#                 )
#             except:
#                 print(df["RETAILER NUMBER"][i], "not in", df["COMPANY"][i].strip())
#                 continue
#         i += 1
